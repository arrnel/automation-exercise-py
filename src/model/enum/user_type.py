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
        user_types = list(UserType)
        user_types.remove(UserType.EMPTY)
        return random.choice(user_types)

    @staticmethod
    def random_except(user_type: "UserType") -> "UserType":
        user_types = set(UserType) - {UserType.EMPTY, user_type}
        return random.choice(list(user_types))
