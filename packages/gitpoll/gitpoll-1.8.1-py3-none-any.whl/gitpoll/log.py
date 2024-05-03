# gitpoll/log.py
import logging
import sys
from logging.handlers import RotatingFileHandler

from . import config as _cfg

def get_logger() -> logging.Logger:
    """Configure and retrieve a logger instance for the application."""
    logger = logging.getLogger(_cfg.LOGGER_NAME)
    logger.setLevel(_cfg.LOGGER_SET_LEVEL)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter(_cfg.LOGGER_FORMAT, datefmt=_cfg.DATE_FORMAT)
    )

    file_handler = RotatingFileHandler(
        _cfg.LOGGER_FILE,
        maxBytes=_cfg.MAX_LOG_SIZE,
        backupCount=_cfg.MAX_LOG_FILES,
    )
    file_handler.setFormatter(
        logging.Formatter(_cfg.LOGGER_FORMAT, datefmt=_cfg.DATE_FORMAT)
    )
    # set date format

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


logger = get_logger()
