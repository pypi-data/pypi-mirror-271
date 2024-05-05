# Logging
import os

LOGGER_FILE = '/tmp/pyshared.log'
LOGGER_NAME = 'pyshared'
MAX_LOG_SIZE = 10 * 1024 * 1024 * 1024  # 10 GB
MAX_LOG_FILES = 3  # Rotate over three files
LOGGER_SET_LEVEL = os.getenv('GET_LOGGER_LEVEL', 'INFO')
# Optimized log format:
# 2024-04-30 06:21 - INFO log.py:get_logger Configured logger instance.

LOGGER_FORMAT = "%(asctime)s %(levelname)s %(module)s:%(funcName)s %(message)s"
DATE_FORMAT = '%m-%d %H:%M:%S'
