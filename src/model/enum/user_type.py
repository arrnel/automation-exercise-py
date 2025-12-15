import random
from enum import Enum


class UserType(Enum):
    EMPTY = ""
    WOMEN = "Women"
    MEN = "Men"
    KIDS = "Kids"

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def random() -> "UserType":
        return random.choice([UserType.WOMEN, UserType.MEN, UserType.KIDS])
