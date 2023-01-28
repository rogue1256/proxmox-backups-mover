import logging
import os

from .utils import get_default_logger_path

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
log_path = os.path.join(get_default_logger_path(), "app.log")
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger = logging.getLogger("main_logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def get_logger():
    return logger
