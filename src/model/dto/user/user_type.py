from pydantic import Field

from src.model.dto.base_model import Model
from src.model.enum.user_type import UserType


class UserTypeDTO(Model):

    usertype: UserType | None = Field(alias="usertype")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(usertype={self.user_type!r})"

    def __str__(self) -> str:
        return self.__repr__()
