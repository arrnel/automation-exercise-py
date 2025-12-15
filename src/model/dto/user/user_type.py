from pydantic import Field

from src.model.base_model import Model
from src.model.user import UserType


class UserTypeDTO(Model):

    user_type: UserType | None = Field(alias="usertype")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(user_type={self.user_type!r})"

    def __str__(self) -> str:
        return self.__repr__()
