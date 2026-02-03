from enum import Enum


class RemoteType(Enum):

    NONE = "none"
    SELENOID = "selenoid"
    MOON = "moon"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    @staticmethod
    def remote_types():
        return {RemoteType.SELENOID, RemoteType.MOON}
