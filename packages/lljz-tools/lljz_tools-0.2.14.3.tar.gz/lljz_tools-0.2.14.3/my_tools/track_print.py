# coding=utf-8
from my_tools.log_manager import LogManager

print_raw = print

__print = LogManager('print', console_level='INFO').get_logger()
def track_print(*args, sep=' ', end='\n', file=None, flush=False):  # noqa
    __print.info(sep.join(map(str, args)), stacklevel=2)


def patch_print():
    try:
        __builtins__.print = track_print
    except AttributeError:
        __builtins__['print'] = track_print


def restore_print():
    try:
        __builtins__.print = track_print
    except AttributeError:
        __builtins__['print'] = track_print


patch_print()
if __name__ == '__main__':
    def add():
        print('Hello World!')


    add()
