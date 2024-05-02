import logging
from enum import Enum


class LogLevel(str, Enum):
    CRITICAL = "critical"
    FATAL = "fatal"
    ERROR = "error"
    WARNING = "warning"
    WARN = "warn"
    INFO = "info"
    DEBUG = "debug"
    NOTSET = "notset"

    def __int__(self):
        match self:
            case "critical":
                return logging.CRITICAL
            case "fatal":
                return logging.FATAL
            case "error":
                return logging.ERROR
            case "warning":
                return logging.WARNING
            case "warn":
                return logging.WARN
            case "info":
                return logging.INFO
            case "debug":
                return logging.DEBUG
            case _:
                return logging.NOTSET
