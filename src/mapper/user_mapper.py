from dataclasses import fields, replace
from typing import cast

from src.model.dto.user.create_user_request import CreateUserRequestDTO
from src.model.dto.user.update_user_request import UpdateUserRequestDTO
from src.model.dto.user.user_response import UserResponseDTO
from src.model.enum.user_title import UserTitle
from src.model.test_data import TestData
from src.model.user import User


class UserMapper:

    @staticmethod
    def to_create_user_request(dto: User) -> CreateUserRequestDTO:
        return CreateUserRequestDTO(
            email=dto.email,
            password=dto.password,
            name=dto.name,
            firstname=dto.first_name,
            lastname=dto.last_name,
            mobile_number=dto.phone_number,
            title=dto.user_title.value if dto.user_title is not None else None,
            birth_day=str(dto.birth_day),
            birth_month=str(dto.birth_month),
            birth_year=str(dto.birth_year),
            company=dto.company,
            country=dto.country,
            state=dto.state,
            city=dto.city,
            address1=dto.address1,
            address2=dto.address2,
            zipcode=dto.zip_code,
        )

    @staticmethod
    def to_update_user_request(dto: User) -> UpdateUserRequestDTO:
        return UpdateUserRequestDTO(
            id=str(dto.id),
            email=dto.email,
            password=dto.password,
            name=dto.name,
            firstname=dto.first_name,
            lastname=dto.last_name,
            mobile_number=dto.phone_number,
            title=dto.user_title.value if dto.user_title else None,
            birth_day=str(dto.birth_day) if dto.birth_day is not None else None,
            birth_month=str(dto.birth_month) if dto.birth_month is not None else None,
            birth_year=str(dto.birth_year) if dto.birth_year is not None else None,
            company=dto.company,
            country=dto.country,
            state=dto.state,
            city=dto.city,
            address1=dto.address1,
            address2=dto.address2,
            zipcode=dto.zip_code,
        )

    @staticmethod
    def to_user(dto: UserResponseDTO, test_data: TestData) -> User:
        return User(
            id=dto.id,
            email=dto.email,
            password=test_data.password,
            name=dto.name,
            first_name=dto.first_name,
            last_name=dto.last_name,
            phone_number=test_data.phone_number,
            user_title=(
                UserTitle(dto.user_title.replace(".", ""))
                if dto.user_title is not None
                else None
            ),
            birth_day=int(dto.birth_day) if dto.birth_day else None,
            birth_month=int(dto.birth_month) if dto.birth_month else None,
            birth_year=int(dto.birth_year) if dto.birth_year else None,
            company=dto.company,
            country=dto.country,
            state=dto.state,
            city=dto.city,
            address1=dto.address1,
            address2=dto.address2,
            zip_code=dto.zip_code,
            test_data=test_data,
        )

    @staticmethod
    def lazy_update_test_data(source: TestData, destination: TestData) -> TestData:
        return TestData(
            csrf=destination.csrf if destination.csrf else source.csrf,
            session_id=(
                destination.session_id if destination.session_id else source.session_id
            ),
            password=destination.password if destination.password else source.password,
            phone_number=(
                destination.phone_number
                if destination.phone_number
                else source.phone_number
            ),
        )

    @staticmethod
    def lazy_update(source: User, destination: User) -> User:
        empty_values = [None, "", [], {}, (), 0]
        update_data = {
            f.name: getattr(destination, f.name)
            for f in fields(User)
            if getattr(destination, f.name) not in empty_values
        }
        return cast(User, replace(source, **update_data)).with_test_data(
            UserMapper.lazy_update_test_data(source.test_data, destination.test_data)
        )
