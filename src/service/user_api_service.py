import logging
from http import HTTPStatus
from typing import Optional

from src.client.core.condition.conditions import Conditions
from src.client.user_api_client import UserApiClient
from src.client.verify_login_api_client import VerifyLoginApiClient
from src.ex.exception import UserNotFoundError
from src.mapper.user_mapper import UserMapper
from src.model.dto.user.user_response import UserResponseDTO
from src.model.test_data import TestData
from src.model.user import User
from src.util.decorator.step_logger import step_log

_USER_EXIST_MESSAGE = "User exists!"
_USER_NOT_EXIST_MESSAGE = "User not found!"


class UserApiService:

    def __init__(self):
        self.user_api_client = UserApiClient()
        self.verify_user_api_client = VerifyLoginApiClient()

    @step_log.log("Create user: {user.email}")
    def create_user(self, user: User) -> User:
        self.user_api_client.send_create_new_user_request(user).check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.CREATED),
        )
        user_response = (
            self.user_api_client.send_get_user_by_email_request(user.email)
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_pojo(cls=UserResponseDTO, path="user")
        )
        user_response = user_response.model_copy(
            update={
                "email": user.email,
                "mobile_phone": user.phone_number,
                "test_data": user.test_data,
            }
        )
        return UserMapper.to_user(user_response, user.test_data)

    @step_log.log("Get user by email: {email}")
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.__get_user(email)

    @step_log.log("Update user with email: {email}")
    def update_user(self, user: User) -> User:
        if not self.__get_user(user.email):
            raise UserNotFoundError(f"User with email = [{user.email}] not found")
        return (
            self.user_api_client.send_update_user_request(user)
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_pojo(User, "user")
        )

    @step_log.log("Delete user with email: {email}")
    def delete_user(self, email: str, password: str) -> None:
        self.user_api_client.send_delete_user_request(email, password).check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
        )

    def safe_delete_user(self, email: str, password: str) -> None:
        try:
            self.delete_user(email, password)
        except Exception as ex:
            logging.info(
                f"Unable to delete user. Email = [{email}], password = [{password}].\n"
                f"Exception: {ex}"
            )

    @step_log.log("Verify login with email = [{email}] and password = [{password}]")
    def verify_login(self, email: str, password: str) -> bool:

        response = self.verify_user_api_client.send_verify_login_request(
            email, password
        )
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
        )
        message = response.extract().as_value("message")

        if message == _USER_EXIST_MESSAGE:
            return True
        elif message == _USER_NOT_EXIST_MESSAGE:
            return False
        else:
            raise ValueError(f"Unexpected response message: {message}")

    def __get_user(self, email: str) -> Optional[User]:

        response = self.user_api_client.send_get_user_by_email_request(email)
        if response.extract().body_status_code() == HTTPStatus.NOT_FOUND:
            return None

        user_response = (
            self.user_api_client.send_get_user_by_email_request(email)
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_pojo(UserResponseDTO, "user")
        )
        return UserMapper.to_user(user_response, TestData.empty())
