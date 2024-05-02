import logging

from .logger import (
    Logger,
    LoggerMixin,
    LogName,
    close,
    get_log,
    get_logpath,
    get_logpaths,
    getLogger,
    load_log,
)
from .models import Event, Log

__version__ = "0.5.0"
__all__ = [
    "Logger",
    "close",
    "get_log",
    "get_logpath",
    "get_logpaths",
    "getLogger",
    "load_log",
    "Event",
    "Log",
    "logging",
    "LoggerMixin",
    "LogName",
]

CRITICAL = logging.CRITICAL
FATAL = CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


logging.setLoggerClass(Logger)
