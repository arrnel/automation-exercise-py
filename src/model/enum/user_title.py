import random
from enum import Enum


class UserTitle(Enum):
    EMPTY = ""
    MR = "Mr"
    MRS = "Mrs"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    @staticmethod
    def random() -> "UserTitle":
        return UserTitle.MR if random.choice([True, False]) else UserTitle.MRS
