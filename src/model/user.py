from dataclasses import dataclass, replace
from datetime import date

from src.model.enum.user_title import UserTitle
from src.model.test_data import TestData


@dataclass
class User:
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
    def empty(cls) -> "User":
        return User(
            id=None,
            email=None,
            password=None,
            name=None,
            first_name=None,
            last_name=None,
            phone_number=None,
            user_title=None,
            birth_day=None,
            birth_month=None,
            birth_year=None,
            company=None,
            country=None,
            state=None,
            city=None,
            address1=None,
            address2=None,
            zip_code=None,
            test_data=None,
        )

    def with_id(self, id: int | None) -> "User":
        return replace(self, id=id)

    def with_password(self, password: str | None) -> "User":
        return replace(self, password=password)

    def with_name(self, name: str | None) -> "User":
        return replace(self, name=name)

    def with_first_name(self, first_name: str | None) -> "User":
        return replace(self, first_name=first_name)

    def with_last_name(self, last_name: str | None) -> "User":
        return replace(self, last_name=last_name)

    def with_email(self, email: str | None) -> "User":
        return replace(self, email=email)

    def with_phone_number(self, phone_number: str | None) -> "User":
        return replace(self, phone_number=phone_number)

    def with_user_title(self, user_title: UserTitle | None) -> "User":
        return replace(self, user_title=user_title)

    def with_birth_day(self, birth_day: int | None) -> "User":
        return replace(self, birth_day=birth_day)

    def with_birth_month(self, birth_month: int | None) -> "User":
        return replace(self, birth_month=birth_month)

    def with_birth_year(self, birth_year: int | None) -> "User":
        return replace(self, birth_year=birth_year)

    def with_birth_date(self, birth_date: date | None) -> "User":
        return replace(
            self,
            birth_day=birth_date.day,
            birth_month=birth_date.month,
            birth_year=birth_date.year
        )

    def with_company(self, company: str | None) -> "User":
        return replace(self, company=company)

    def with_country(self, country: str) -> "User":
        return replace(self, country=country)

    def with_state(self, state: str | None) -> "User":
        return replace(self, state=state)

    def with_city(self, city: str | None) -> "User":
        return replace(self, city=city)

    def with_address1(self, address1: str | None) -> "User":
        return replace(self, address1=address1)

    def with_address2(self, address2: str | None) -> "User":
        return replace(self, address2=address2)

    def with_zip_code(self, zip_code: str | None) -> "User":
        return replace(self, zip_code=zip_code)

    def with_test_data(self, test_data: TestData | None) -> "User":
        return replace(self, test_data=test_data)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{id=}, "
            f"{self.email=}, "
            f"{self.first_name=}, "
            f"{self.last_name=}"
            ")"
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
            f"zip_code={self.zip_code!r},\n"
            f"test_data={self.test_data!r}"
            f")"
        )
