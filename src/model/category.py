from pydantic import Field

from src.model.base_model import Model
from src.model.user import UserTypeDTO, UserType


class CategoryDTO(Model):
    usertype: UserTypeDTO = Field(alias="usertype")
    category: str = Field(alias="category")

    @classmethod
    def of(cls, usertype: UserType, category: str) -> "CategoryDTO":
        return CategoryDTO(usertype=UserTypeDTO(usertype=usertype), category=category)

    def __repr__(self) -> str:
        return f"CategoryDTO(usertype={self.usertype!r}, category={self.category!r})"

    def __str__(self) -> str:
        return self.__repr__()
