import logging
import os
import sys
import re
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from os import PathLike
from pathlib import Path
from typing import TextIO, Callable, Optional, Mapping, IO, Any

from colorlog import ColoredFormatter as CF
from my_tools.color import Color


class ColoredFormatter(CF):

    def __init__(
            self,
            fmt: Optional[str] = None,
            datefmt: Optional[str] = None,
            log_colors: Optional[dict] = None,
            reset: bool = True,
            secondary_log_colors: Optional[dict] = None,
    ) -> None:
        secondary_log_colors = {
            k: ({lv: v for lv in logging._nameToLevel} if isinstance(v, str) else v)
            for k, v in secondary_log_colors.items()
        }
        for k in secondary_log_colors.keys():
            fmt = re.sub(rf'({{{k}.*?}})', rf'{{{k}_log_color}}\1{{reset}}', fmt)
        super().__init__(
            fmt=fmt,
            datefmt=datefmt,
            style='{',
            log_colors=log_colors,
            reset=reset,
            secondary_log_colors=secondary_log_colors,
        )

    def format(self, record):
        if record.exc_info:

            if not record.exc_text:
                record.exc_text = Color.thin_red(self.formatException(record.exc_info))
            elif isinstance(record.exc_text, str) and not record.exc_text.startswith('\033['):
                record.exc_text = Color.thin_red(record.exc_text)
        return super().format(record)


ColoredFormatter.default_msec_format = '%s.%03d'
Formatter.default_msec_format = '%s.%03d'

TRACE = 5
SUCCESS = 25
logging.addLevelName(TRACE, "TRACE")
logging.addLevelName(SUCCESS, "SUCCESS")

default_console_format = ColoredFormatter(
    '{asctime} | {levelname:<8} | {name} | {module}:{funcName}:{lineno} - {message}',
    secondary_log_colors={
        "levelname": {
            'TRACE': 'cyan',
            'DEBUG': 'blue',
            'SUCCESS': 'light_green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bg_red',
        },
        "message": {
            'TRACE': 'cyan',
            'DEBUG': 'blue',
            'SUCCESS': 'light_green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bg_red',
        },
        "asctime": 'green',
        "name": 'cyan',
        "module": 'cyan',
        "funcName": 'cyan',
        "lineno": 'cyan',
    },
    )
default_file_format = Formatter(
    '{asctime} | {levelname:<8} | {name} | {module}:{funcName}:{lineno} - {message}',
    style='{'
)


class ManagerLogger(logging.Logger):

    def catch_exception(self, func: Callable):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.exception(e, stacklevel=2)

        return inner

    def _add_console_handler(self, stream=None, level=None, formatter: str | Formatter = None,
                             filters: Callable | list[Callable] = None):
        if stream is None:
            stream = sys.stdout
        handler = logging.StreamHandler(stream)
        if not formatter:
            formatter = default_console_format
        if isinstance(formatter, str):
            formatter = Formatter(formatter)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        if filters is not None:
            if isinstance(filters, Callable):
                filters = [filters]
            for f in filters:
                handler.addFilter(f)
        self.addHandler(handler)

    def _add_file_handler(self, path: str | PathLike, level=None, formatter: str | Formatter = None,
                          filters: Callable | list[Callable] = None):
        handler = TimedRotatingFileHandler(
            path,
            when="midnight",
            backupCount=10,
            encoding="utf-8",
            delay=True,
        )
        handler.setLevel(level)
        if not formatter:
            formatter = default_file_format
        if isinstance(formatter, str):
            formatter = Formatter(formatter)
        handler.setFormatter(formatter)
        if filters is not None:
            if isinstance(filters, Callable):
                filters = [filters]
            for f in filters:
                handler.addFilter(f)
        self.addHandler(handler)

    def remove(self, handler=None):
        if handler:
            return self.removeHandler(handler)
        for handler in self.handlers:
            self.removeHandler(handler)

    def add(self, sink: TextIO | str | PathLike, *, level: int | str = "DEBUG", formatter=None, filters=None):
        if sink == sys.stdout or sink == sys.stderr:
            return self._add_console_handler(sink, level=level, filters=filters, formatter=formatter)
        return self._add_file_handler(sink, level=level, filters=filters, formatter=formatter)

    def success(self, msg, *args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        return self._log(
            SUCCESS, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel + 1
        )

    def trace(self, msg, *args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        return self._log(
            TRACE, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, stacklevel=stacklevel + 1
        )


class LogManager:

    def __init__(
            self, __name, *,
            console_level: int | str = "DEBUG",
            file_path: str = None,
            file_level: int | str | None = "DEBUG",
            error_level: int | str | None = "ERROR"
    ) -> None:
        logging.root.setLevel(logging.NOTSET)
        self._file_path = self._init_log_file_path(file_path)
        self.console_level = console_level
        self.file_level = file_level
        self.error_level = error_level
        __logger = logging.getLogger(__name)
        self._logger = ManagerLogger(__logger.name, __logger.level)

    @staticmethod
    def _init_log_file_path(file_path: str | PathLike = None) -> Path:
        if file_path:
            return Path(file_path)
        if "PYTHONPATH" in os.environ and os.path.exists(os.environ['PYTHONPATH']):
            path = Path(os.environ['PYTHONPATH']) / 'logs'
            if not path.exists():
                os.mkdir(path)
            return path
        path = Path('/pythonlogs')
        if not path.exists():
            os.mkdir(path)
        return path

    def get_logger(self, reset=False) -> ManagerLogger:
        if reset:
            self._logger.remove()
        if not self._logger.handlers:
            self._logger.add(sys.stdout, level=self.console_level)
            if self.file_level:
                self._logger.add(self._file_path / 'out.log', level=self.file_level)
            if self.error_level:
                self._logger.add(self._file_path / 'error.log', level=self.error_level)
        return self._logger


if __name__ == '__main__':
    logger = LogManager(__name__, console_level=TRACE).get_logger()

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
    logger.success('succee!')
    logger.trace('trace message')


    def get(url):
        logger.debug('GET - %s', url, stacklevel=2)


    @logger.catch_exception
    def todo():
        get('http://www.baidu.com')
        print(1 / 0)


    todo()