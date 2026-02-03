from dataclasses import dataclass

from src.model.enum.user_type import UserType


@dataclass
class Category:

    user_type: UserType | None
    title: str | None

    def __str__(self):
        return (
            f"{self.__class__.__name__}("
            f"user_type={self.user_type}, "
            f"title={self.title}"
            ")"
        )

    def __repr__(self):
        return self.__str__()
