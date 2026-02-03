from pydantic import Field

from src.model.dto.base_model import Model
from src.model.dto.user.user_type import UserTypeDTO
from src.model.enum.user_type import UserType


class CategoryResponseDTO(Model):
    usertype: UserTypeDTO = Field()
    category: str = Field()

    @classmethod
    def of(cls, usertype: UserType, category: str) -> "CategoryResponseDTO":
        return CategoryResponseDTO(
            usertype=UserTypeDTO(usertype=usertype), category=category
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"usertype={self.usertype!r},\n"
            f"category={self.category!r}\n"
            f")"
        )

    def __str__(self) -> str:
        return self.__repr__()
