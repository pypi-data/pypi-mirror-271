##
##

import os
import sys
import inspect
import logging
import traceback
from datetime import datetime
from pytoolbase.config import get_log_dir

logger = logging.getLogger('pytoolbase.exception')
logger.addHandler(logging.NullHandler())


class NonFatalError(Exception):

    def __init__(self, message):
        frame = inspect.currentframe().f_back
        (filename, line, function, lines, index) = inspect.getframeinfo(frame)
        filename = os.path.basename(filename)
        self.message = f"Error: {type(self).__name__} in {filename} {function} at line {line}: {message}"
        super().__init__(self.message)


class FatalError(Exception):

    def __init__(self, message):
        frame = inspect.currentframe().f_back
        (filename, line, function, lines, index) = inspect.getframeinfo(frame)
        filename = os.path.basename(filename)
        logging.debug(f"Error: {type(self).__name__} in {filename} {function} at line {line}: {message}")
        logging.error(f"{message} [{filename}:{line}]")

        crash_log_file = os.path.join(get_log_dir(), "crash.log")
        logging.debug(f"See {crash_log_file} for stack trace")

        with open(crash_log_file, 'a') as log:
            now = datetime.now()
            time_string = now.strftime("%D %I:%M:%S %p")
            log.write(f"---- BEGIN {time_string} ----\n")
            log.write(f"== <ERROR> ==\n")
            log.write(f"{message} [{filename}:{line}]\n")
            trace_output = traceback.format_exc()
            if trace_output:
                log.write(f"== <TRACE> ==\n")
                log.write(trace_output)
            log.write(f"---- END ----\n")
            log.flush()

        sys.exit(1)
