# gitpoll/log.py
import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from typing import Optional as Opt
from . import _config as _cfg


def get_logger(
    name: str = _cfg.LOGGER_NAME,
    level: Opt[str] = None,
    fmt: str = _cfg.LOGGER_FORMAT,
    datefmt: str = _cfg.DATE_FORMAT,
    console: bool = True,
    file: bool = True,
) -> logging.Logger:
    """Configure and retrieve a logger instance for the application.
    ~name (str): Name of the logger.
        Default: 'pyshared'
    ~level (Optional[str]): Logging level for the logger.
        Uses GET_LOGGER_LEVEL environment variable if not set.
        Default: None
    ~fmt (str): Format string for the logger.
        Default: %(asctime)s %(levelname)s %(module)s:%(funcName)s %(message)s
    ~datefmt (str): Date format for the logger.
        Default: '%m-%d %H:%M:%S'
    ~console (bool): Enable console logging.
        Default: True
    ~file (bool): Enable file logging.
        Default: True
    -> logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(
        level if level is not None else os.getenv('GET_LOGGER_LEVEL', 'INFO')
    )

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
        logger.addHandler(console_handler)

    if file:
        file_handler = RotatingFileHandler(
            _cfg.LOGGER_FILE,
            maxBytes=_cfg.MAX_LOG_SIZE,
            backupCount=_cfg.MAX_LOG_FILES,
        )
        file_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
        logger.addHandler(file_handler)
    return logger
