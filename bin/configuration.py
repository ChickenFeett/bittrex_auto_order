from enum import IntEnum


class Config:
    class LoggingModes(IntEnum):
        OFF = 0
        FATAL = 1
        ERROR = 2
        WARN = 3
        INFO = 4
        DEBUG = 5
        TRACE = 6
        ALL = 7

    debug_mode = False
    logging = LoggingModes.ERROR

