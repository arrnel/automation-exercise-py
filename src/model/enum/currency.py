from enum import Enum


class Currency(Enum):
    RS = "Rs"

    def __str__(self) -> str:
        return self.value
