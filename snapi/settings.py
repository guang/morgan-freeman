from datetime import datetime
import logging
import os
import sys


HEADER = """
SNAPI
"""

LOGGING_LEVEL = logging.DEBUG
LOGGING_FILE = "{home}/snapi_{current_time}.log".format(home=os.environ['HOME'], current_time=datetime.now().strftime("%Y%m%d"))
LOGGING_FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'
LOGGING_MODE = 'a'


def configure_logging(log_level=LOGGING_LEVEL, log_format=LOGGING_FORMAT, log_file=LOGGING_FILE, log_mode=LOGGING_MODE):

    root_logger = logging.getLogger('snapi')
    root_logger.setLevel(log_level)

    formatter = logging.Formatter(log_format)

    stdout_log_handler = logging.StreamHandler(sys.stdout)
    stdout_log_handler.setLevel(log_level)
    stdout_log_handler.setFormatter(formatter)
    root_logger.addHandler(stdout_log_handler)

    if log_file:
        file_log_handler = logging.FileHandler(log_file, mode=log_mode)
        file_log_handler.setLevel(log_level)
        file_log_handler.setFormatter(formatter)
        root_logger.addHandler(file_log_handler)

    return root_logger


snapi_logger = configure_logging()
