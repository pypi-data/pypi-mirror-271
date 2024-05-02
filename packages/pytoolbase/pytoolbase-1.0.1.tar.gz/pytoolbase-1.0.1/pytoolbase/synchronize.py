##
##

import logging
import threading
from typing import Callable
from functools import wraps

logger = logging.getLogger('pytoolbase.synchronize')
logger.addHandler(logging.NullHandler())
lock = threading.Lock()


def synchronize() -> Callable:
    def lock_handler(func):
        @wraps(func)
        def f_wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return f_wrapper
    return lock_handler


class Synchronize(object):

    def __init__(self):
        pass

    def __enter__(self):
        lock.acquire()

    def __exit__(self, *args):
        lock.release()
