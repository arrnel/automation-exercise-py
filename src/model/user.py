import random
from dataclasses import dataclass, replace
from datetime import date
from enum import Enum

from pydantic import Field

from src.model.base_model import Model
from src.model.test_data import TestData


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


class UserTypeDTO(Model):

    user_type: UserType | None = Field(alias="usertype")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(user_type={self.user_type!r})"

    def __str__(self) -> str:
        return self.__repr__()

@dataclass
class UserDTO:
    id: int | None
    email: str | None
    password: str | None
    name: str | None
    first_name: str | None
    last_name: str | None
    phone_number: str | None
    user_title: UserTitle | None
    birth_day: int | None
    birth_month: int | None
    birth_year: int | None
    company: str | None
    country: str | None
    state: str | None
    city: str | None
    address1: str | None
    address2: str | None
    zip_code: str | None
    test_data: TestData | None

    @classmethod
    def empty(cls) -> "UserDTO":
        return UserDTO(
            id=None,
            email=None,
            password=None,
            name=None,
            first_name=None,
            last_name=None,
            phone_number=None,
            user_title = None,
            birth_day = None,
            birth_month = None,
            birth_year = None,
            company = None,
            country = None,
            state = None,
            city = None,
            address1 = None,
            address2 = None,
            zip_code = None,
            test_data = None,
        )

    def with_id(self, id: int | None) -> "UserDTO":
        return replace(self, id=id)

    def with_password(self, password: str | None) -> "UserDTO":
        return replace(self, password=password)

    def with_name(self, name: str | None) -> "UserDTO":
        return replace(self, name=name)

    def with_first_name(self, first_name: str | None) -> "UserDTO":
        return replace(self, first_name=first_name)

    def with_last_name(self, last_name: str| None) -> "UserDTO":
        return replace(self, last_name=last_name)

    def with_email(self, email: str| None) -> "UserDTO":
        return replace(self, email=email)

    def with_phone_number(self, phone_number: str| None) -> "UserDTO":
        return replace(self, phone_number=phone_number)

    def with_user_title(self, user_title: UserTitle| None) -> "UserDTO":
        return replace(self, user_title=user_title)

    def with_birth_day(self, birth_day: int| None) -> "UserDTO":
        return replace(self, birth_day=birth_day)

    def with_birth_month(self, birth_month: int| None) -> "UserDTO":
        return replace(self, birth_month=birth_month)

    def with_birth_year(self, birth_year: int| None) -> "UserDTO":
        return replace(self, birth_year=birth_year)

    def with_birth_date(self, birth_date: date| None) -> "UserDTO":
        return replace(
            self,
            birth_day=birth_date.day,
            birth_month= birth_date.month,
            birth_year=birth_date.year
        )

    def with_company(self, company: str| None) -> "UserDTO":
        return replace(self, company=company)

    def with_country(self, country: str) -> "UserDTO":
        return replace(self, country=country)

    def with_state(self, state: str| None) -> "UserDTO":
        return replace(self, state=state)

    def with_city(self, city: str| None) -> "UserDTO":
        return replace(self, city=city)

    def with_address1(self, address1: str| None) -> "UserDTO":
        return replace(self, address1=address1)

    def with_address2(self, address2: str| None) -> "UserDTO":
        return replace(self, address2=address2)

    def with_zip_code(self, zip_code: str| None) -> "UserDTO":
        return replace(self, zip_code=zip_code)

    def with_test_data(self, test_data: TestData | None) -> "UserDTO":
        return replace(self, test_data=test_data)

    def __repr__(self) -> str:
        return f"UserDTO({id=}, {self.email=}, {self.first_name=}, {self.last_name=}"

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
            f"zip_code={self.zip_code!r},\n"
            f"test_data={self.test_data!r}"
            f")"
        )

class CreateUserRequestDTO(Model):
    email: str | None = Field(alias="email")
    password: str | None = Field(alias="password")
    name: str | None = Field(alias="name")
    first_name: str | None = Field(alias="firstname")
    last_name: str | None = Field(alias="lastname")
    mobile_number: str | None = Field(alias="mobile_number")
    user_title: str | None = Field(alias="title")
    birth_day: str | None = Field(alias="birth_day")
    birth_month: str | None = Field(alias="birth_month")
    birth_year: str | None = Field(alias="birth_year")
    company: str | None = Field(alias="company")
    country: str | None = Field(alias="country")
    state: str | None = Field(alias="state")
    city: str | None = Field(alias="city")
    address1: str | None = Field(alias="address1")
    address2: str | None = Field(alias="address2")
    zip_code: str | None = Field(alias="zipcode")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.email=}, {self.first_name=}, {self.last_name=}"

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
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
            f"zipcode={self.zip_code!r}\n"
            f")"
        )

class UpdateUserRequestDTO(Model):
    id: str | None = Field(alias="id")
    email: str | None = Field(alias="email")
    password: str | None = Field(alias="password")
    name: str | None = Field(alias="name")
    first_name: str | None = Field(alias="firstname")
    last_name: str | None = Field(alias="lastname")
    mobile_number: str | None = Field(alias="mobile_number")
    user_title: str | None = Field(alias="title")
    birth_day: str | None = Field(alias="birth_day")
    birth_month: str | None = Field(alias="birth_month")
    birth_year: str | None = Field(alias="birth_year")
    company: str | None = Field(alias="company")
    country: str | None = Field(alias="country")
    state: str | None = Field(alias="state")
    city: str | None = Field(alias="city")
    address1: str | None = Field(alias="address1")
    address2: str | None = Field(alias="address2")
    zip_code: str | None = Field(alias="zipcode")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({id=}, {self.email=}, {self.first_name=}, {self.last_name=}"

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
            f"zipcode={self.zip_code!r}\n"
            f")"
        )

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
        return f"{self.__class__.__name__}({id=}, {self.email=}, {self.first_name=}, {self.last_name=}"

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