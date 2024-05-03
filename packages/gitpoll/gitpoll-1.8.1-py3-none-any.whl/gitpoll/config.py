# Logging
import os

LOGGER_FILE = 'gitpoll.log'
LOGGER_NAME = 'gitpoll'
MAX_LOG_SIZE = 10 * 1024 * 1024 * 1024  # 10 GB
MAX_LOG_FILES = 3  # Rotate over three files
LOGGER_SET_LEVEL = 'DEBUG'
# Optimized log format: Date-Time Level[Logger]Module:Function:Line-Message
# Example output: 2024-04-30 06:21 - INFO[gitpoll]main:main:22-Checking for changes in the repository.
LOGGER_FORMAT = "%(asctime)s %(levelname)s %(module)s:%(funcName)s %(message)s"
DATE_FORMAT = '%m-%d %H:%M:%S'
