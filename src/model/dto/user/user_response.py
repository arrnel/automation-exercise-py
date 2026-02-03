from pydantic import Field

from src.model.dto.base_model import Model


class UserResponseDTO(Model):
    id: int | None = Field(alias="id")
    name: str | None = Field(alias="name")
    email: str | None = Field(alias="email")
    user_title: str | None = Field(alias="title")
    birth_day: str | None = Field(alias="birth_day")
    birth_month: str | None = Field(alias="birth_month")
    birth_year: str | None = Field(alias="birth_year")
    first_name: str | None = Field(alias="first_name")
    last_name: str | None = Field(alias="last_name")
    company: str | None = Field(alias="company")
    address1: str | None = Field(alias="address1")
    address2: str | None = Field(alias="address2")
    country: str | None = Field(alias="country")
    state: str | None = Field(alias="state")
    city: str | None = Field(alias="city")
    zip_code: str | None = Field(alias="zipcode")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{id=}, "
            f"{self.email=}, "
            f"{self.first_name=}, "
            f"{self.last_name=}"
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id!r},\n"
            f"email={self.email!r},\n"
            f"password={self.password!r},\n"
            f"name={self.name!r},\n"
            f"first_name={self.first_name!r},\n"
            f"last_name={self.last_name!r},\n"
            f"phone_number={self.phone_number!r},\n"
            f"user_title={self.user_title!r},\n"
            f"birth_day={self.birth_day!r},\n"
            f"birth_month={self.birth_month!r},\n"
            f"birth_year={self.birth_year!r},\n"
            f"company={self.company!r},\n"
            f"country={self.country!r},\n"
            f"state={self.state!r},\n"
            f"city={self.city!r},\n"
            f"address1={self.address1!r},\n"
            f"address2={self.address2!r},\n"
            f"zip_code={self.zip_code!r}\n"
            f")"
        )
