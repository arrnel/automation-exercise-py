from pydantic import Field

from src.model.dto.base_model import Model

_CSRF_KEY = "csrfmiddlewaretoken"


class CredentialsRequestDTO(Model):

    csrf: str | None = Field(alias=_CSRF_KEY)
    email: str | None = Field(alias="email")
    password: str | None = Field(alias="password")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.csrf=}, {self.email=}, {self.password=}"
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{_CSRF_KEY}={self.csrf!r}, "
            f"email={self.email!r}, "
            f"password={self.password!r}, "
            ")"
        )
