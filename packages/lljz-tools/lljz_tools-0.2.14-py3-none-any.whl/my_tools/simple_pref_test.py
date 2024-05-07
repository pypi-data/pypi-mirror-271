# coding=utf-8

"""
@fileName       :   simple_pref_test.py
@data           :   2024/4/19
@author         :   jiangmenggui@hosonsoft.com
"""
import json
import math
import os.path
import queue
import random
import sys
import time
from collections import defaultdict
from inspect import isfunction
from pathlib import Path
from typing import NamedTuple

# from concurrent.futures import ThreadPoolExecutor
import gevent
from gevent.threadpool import ThreadPoolExecutor

from my_tools import logger
from my_tools.color import Color
from my_tools.console_table import ConsoleTable
from my_tools.decorators import catch_exception

data: queue.Queue["TaskResult"] = queue.Queue()
start_time = time.time()
end_time: float | None = None


class TaskResult(NamedTuple):
    name: str
    start: float
    end: float
    message: str = ""
    success: bool = True

    @property
    def use_time(self):
        return self.end - self.start


def task(name: str, weight=1):
    """
    测试任务
    :param name: 任务名称
    :param weight: 任务执行权重
    :return:
    """
    if not name:
        raise ValueError("任务名称（name参数）不能为空")

    if not isinstance(weight, int) or weight < 0:
        raise ValueError("任务权重（weight参数）必须为大于0的整数")

    def outer(func):
        def inner(*args, **kwargs):
            t1 = time.time()
            try:
                func(*args, **kwargs)
                t2 = time.time()
                data.put(TaskResult(name=name, start=t1, end=t2))
            except Exception as e:
                t2 = time.time()
                data.put(
                    TaskResult(name=name, start=t1, end=t2, message=f'{e.__class__.__name__}: {str(e)}', success=False)
                )
                logger.exception(e, stacklevel=1)

        inner.is_task = True
        inner.weight = weight
        return inner

    return outer


def show_result():
    result: dict[str, dict] = {}
    tps: dict[str, dict[str, int]] = {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)): defaultdict(int) for i in
                                      range(int(start_time), int(end_time) + 1)}
    response: dict[str, dict[str, list]] = {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i)): defaultdict(list) for
                                            i in
                                            range(int(start_time), int(end_time) + 1)}
    while not data.empty():
        row = data.get()
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row.end))
        if t not in tps:
            tps[t] = defaultdict(int)
        if t not in response:
            response[t] = defaultdict(list)
        response[t][row.name].append(row.use_time)
        if row.success:
            tps[t][row.name + '(成功)'] += 1
        else:
            tps[t][row.name + '(失败)'] += 1
        if row.name not in result:
            result[row.name] = {
                "NAME": row.name,
                "START_TIME": row.start,
                "END_TIME": row.end,
                "USE_TIME": [row.use_time],
                "SUCCESS": int(bool(row.success))
            }
        else:
            result[row.name]['START_TIME'] = min(result[row.name]['START_TIME'], row.start)
            result[row.name]['END_TIME'] = max(result[row.name]['END_TIME'], row.end)
            result[row.name]['USE_TIME'].append(row.use_time)
            result[row.name]['SUCCESS'] += int(bool(row.success))
    table_data = []
    for value in result.values():
        use_time = sorted(value["USE_TIME"])
        table_data.append({
            "任务名称": value['NAME'],
            "任务执行次数": len(use_time),
            "事务成功数": value['SUCCESS'],
            "事务成功率": f"{value['SUCCESS'] / len(use_time):.2%}",
            "中位数响应(ms)": f"{use_time[int(len(use_time) * 0.5)] * 1000:.1f}ms",
            "90%响应(ms)": f"{use_time[int(len(use_time) * 0.9)] * 1000:.1f}ms",
            "95%响应(ms)": f"{use_time[int(len(use_time) * 0.95)] * 1000:.1f}ms",
            "平均响应(ms)": f"{sum(value['USE_TIME']) * 1000 / len(value['USE_TIME']):.1f}ms",
            "最小响应(ms)": f"{use_time[0] * 1000:.1f}ms",
            "最大响应(ms)": f"{use_time[-1] * 1000:.1f}ms",

        })
    table = ConsoleTable(table_data, caption="性能测试结果")
    print(table)
    return table, table_data, tps, response


class TaskNotFoundError(ValueError): ...


class PrefRunner:
    """
    测试性能
    :param modules: 测试模块
    :param virtual_users: 虚拟用户数
    :param user_add_interval: 用户增加间隔
    :param run_seconds: 测试时间
    :param pre_task: 每秒执行的任务数量，和virtual_users参数互斥，该参数不为空时，则按照每秒执行的任务数量来执行
    :param save_result_directory: 保存结果目录，默认在当前目录下的simple_pref_test_result目录
    """

    def __init__(
            self,
            *modules,
            has_main_module=True,
            virtual_users=10,
            user_add_interval=0.1,
            pre_task: int = None,
            run_seconds=10,
            save_result_directory='./simple_pref_test_result',
    ):
        self.tasks = []
        if has_main_module:
            modules = (*modules, sys.modules['__main__'])
        for module in modules:
            for v in module.__dict__.values():
                if isfunction(v) and getattr(v, 'is_task', False):
                    self.tasks.extend((v for _ in range(getattr(v, 'weight', 1))))
        if not self.tasks:
            raise TaskNotFoundError('没有识别到测试任务！')
        self.run_seconds = run_seconds
        self.user_add_interval = user_add_interval
        self.virtual_users = virtual_users
        self.save_result_directory = os.path.abspath(save_result_directory)

        self.pool = ThreadPoolExecutor(virtual_users)
        self._start_time = 0
        self.pre_task = pre_task
        self.running = True

    def run_task(self, *args, **kwargs):
        if self.pre_task:
            self._run_task_with_pre_task(*args, **kwargs)
        else:
            self._run_task_with_virtual_users(*args, **kwargs)

    def _run_task_with_virtual_users(self, *args, **kwargs):
        def run(*args, **kwargs):  # noqa
            while time.time() - self._start_time < self.run_seconds and self.running:
                random.choice(self.tasks)(*args, **kwargs)

        for _ in range(self.virtual_users):
            self.pool.submit(run, *args, **kwargs)
            gevent.sleep(self.user_add_interval)

    def _run_task_with_pre_task(self, *args, **kwargs):
        def run(*args, **kwargs):  # noqa
            random.choice(self.tasks)(*args, **kwargs)

        x, y = divmod(self.pre_task, 10)
        ts = [x] * 10
        for i in range(y):
            ts[i] += 1
        while time.time() - self._start_time < self.run_seconds and self.running:
            for t in ts:
                for _ in range(t):
                    self.pool.submit(run, *args, **kwargs)
                gevent.sleep(0.093)

    @catch_exception()
    def start(self, *args, **kwargs):
        global end_time
        self._start_time = time.time()
        start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._start_time))
        if self.pre_task:

            print(
                f"{Color.yellow('==========测试任务启动参数==========')}\n"
                f"   {Color.thin_magenta('每秒任务数')} : {self.pre_task}\n"
                f"     {Color.thin_magenta('运行时间')} : {self.run_seconds}s\n"
                f"     {Color.thin_magenta('任务总数')} : {len(set(self.tasks))}\n"
                f"     {Color.thin_magenta('启动时间')} : {start_time_str}\n"
                f"{Color.yellow('====================================')}\n"
            )
        else:
            print(
                f"{Color.yellow('==========测试任务启动参数==========')}\n"
                f"   {Color.thin_magenta('并发线程数')} : {self.virtual_users}\n"
                f" {Color.thin_magenta('线程启动间隔')} : {self.user_add_interval}s\n"
                f"     {Color.thin_magenta('运行时间')} : {self.run_seconds}s\n"
                f"     {Color.thin_magenta('任务总数')} : {len(set(self.tasks))}\n"
                f"     {Color.thin_magenta('启动时间')} : {start_time_str}\n"
                f"{Color.yellow('====================================')}\n"
            )
        try:
            self.run_task(*args, **kwargs)
            self.pool.shutdown(wait=True)
        finally:
            end_time = time.time()
            table, table_data, tps, response = show_result()
            end_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            end_str = f'\n{Color.green("测试完成！")}[完成时间{Color.thin_cyan(end_time_str)}]'
            print('\n' + end_str)
            self._save(table_data, tps, response)

    def _save_html(self, file, table, tps, response):

        def init_tps_data(tps):
            tps = sorted(tps.items())
            keys = set()
            for _, v in tps:
                for k in v:
                    keys.add(k)
            values = {k: [] for k in keys}
            for _, v in tps:
                for k in keys:
                    values[k].append(v.get(k, 0))
            return json.dumps({
                'keys': [k.split(' ')[1] for k, v in tps],
                "values": [{"name": k, "data": v} for k, v in values.items()]
            }, ensure_ascii=False)

        def init_response_data(response):
            response = sorted(response.items())
            keys = set()
            for _, v in response:
                for k in v:
                    keys.add(k)
            values = {k: [] for k in keys}
            for _, v in response:
                for k in keys:
                    v_ = v.get(k, [0])
                    values[k].append(int(sum(v_) / len(v_) * 1000))
            return json.dumps({
                'keys': [k.split(' ')[1] for k, v in response],
                "values": [{"name": k, "data": v} for k, v in values.items()]
            }, ensure_ascii=False)

        def init_table_data(table_data):
            return {"header": list(table_data[0].keys()), "rows": [list(row.values()) for row in table_data]}

        from jinja2 import Environment, FileSystemLoader, select_autoescape

        # 创建一个环境，指定模板文件所在的路径
        env = Environment(
            loader=FileSystemLoader(Path(__file__).parent),
            autoescape=select_autoescape(['html', 'xml'])
        )
        if self.pre_task:
            run_arguments = [
                f"每秒任务数 : {self.virtual_users}"
            ]
        else:
            run_arguments = [
                f"并发线程数 : {self.virtual_users}",
                f"线程启动间隔 : {self.user_add_interval}s"
            ]

        template = env.get_template('result.html')
        context = {
            'arguments': [
                *run_arguments,
                f"运行时间 : {self.run_seconds}s",
                f"任务总数 : {len(set(self.tasks))}",
                f"启动时间 : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}",
                f"结束时间 : {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}"],
            "table": init_table_data(table),
            "tpsData": init_tps_data(tps),
            "responseData": init_response_data(response)
        }
        with open(file, 'w', encoding='u8') as f:
            f.write(template.render(context))

    def _save(self, table, tps, response):
        if not os.path.exists(self.save_result_directory):
            os.mkdir(self.save_result_directory)
        file = os.path.join(self.save_result_directory, f'result_{time.strftime("%Y%m%d%H%M%S")}')
        self._save_html(file + '.html', table, tps, response)
        print(f'\n结果已保存至：{Color.thin_blue(file + ".html")}')


if __name__ == '__main__':
    print(math.ceil(3 / 10))
