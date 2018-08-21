from enum import IntEnum


class LoggingModes(IntEnum):
    OFF = 0
    FATAL = 1
    ERROR = 2
    WARN = 3
    INFO = 4
    DEBUG = 5
    TRACE = 6
    ALL = 7

class Config:
    EXPECTED_API_KEY_LENGTH = 32
    EXPECTED_SECRET_KEY_LENGTH = 32

    debug_mode = False
    logging = LoggingModes.ERROR

