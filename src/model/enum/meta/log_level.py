from enum import Enum


class LogLvl(Enum):
    FATAL = 50
    ERROR = 40
    WARN = 30
    INFO = 20
    DEBUG = 10

    @property
    def code(self) -> int:
        return self.value


class ApiLogLvl(Enum):
    NONE = 0
    HEADERS = 1
    BODY = 2
    ALL = 3
