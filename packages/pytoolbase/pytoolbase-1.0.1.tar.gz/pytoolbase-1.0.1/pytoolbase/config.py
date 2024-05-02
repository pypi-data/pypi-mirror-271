##
##

import os
from pathlib import Path

LOG_DIRECTORY = Path.home()


def get_log_dir():
    if 'DEBUG_LOG_DIRECTORY' in os.environ:
        return os.environ['DEBUG_LOG_DIRECTORY']
    else:
        return LOG_DIRECTORY


def set_log_dir(directory):
    global LOG_DIRECTORY
    LOG_DIRECTORY = directory
