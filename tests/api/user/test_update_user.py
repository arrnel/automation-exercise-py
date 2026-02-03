from http import HTTPStatus

import allure
import pytest

from src.client.core.condition.conditions import Conditions
from src.mapper.user_mapper import UserMapper
from src.model.user import User
from src.util.decorator.disabled_by_issue import disabled_by_issue
from src.util.test.data_generator import DataGenerator
from tests.api.base_api_test import BaseApiTest
from tests.data_provider.user_data_provider import UserDataProviderApi

ACCOUNT_NOT_FOUND_MESSAGE = "Account not found!"
SUCCESSFUL_UPDATE_MESSAGE = "User updated!"


@pytest.mark.user_test
@allure.feature("User")
class TestUpdateUserApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Update user with valid data")
    @allure.title(
        "[API] Update user should return 200_OK "
        "when send update user request with valid data. "
        "Case: {case_title}"
    )
    @pytest.mark.parametrize(
        "case_title,user_to_update",
        UserDataProviderApi.valid_sensitive_data_provider(),
        ids=[param[0] for param in UserDataProviderApi.valid_sensitive_data_provider()],
    )
    def test_update_user_with_valid_data(
        self,
        case_title: str,
        user_to_update: User,
        create_user,
    ):

        # Data
        user = (
            DataGenerator.random_user()
            .with_id(create_user.id)
            .with_email(create_user.email)
            .with_test_data(create_user.test_data)
        )

        # Steps
        response = self.user_api_client.send_update_user_request(user)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            Conditions.body_field_equals("message", SUCCESSFUL_UPDATE_MESSAGE),
        )

    @disabled_by_issue(issue_id=1, reason="[WEB] Not validate sensitive data")
    @allure.label("owner", "arrnel")
    @allure.story("Update user with invalid data")
    @allure.title(
        "[API] Update user should return 400_BAD_REQUEST "
        "when send update user request with invalid data. "
        "Case: {case_title}"
    )
    @pytest.mark.parametrize(
        "case_title,user_to_update,expected_message",
        UserDataProviderApi.invalid_sensitive_data_provider(),
        ids=[
            param[0] for param in UserDataProviderApi.invalid_sensitive_data_provider()
        ],
    )
    def test_not_update_user_with_invalid_data(
        self,
        case_title: str,
        user_to_update: User,
        expected_message: str,
        create_user: User,
    ):

        # Data
        new_user = UserMapper.lazy_update(
            create_user,
            user_to_update.with_email(create_user.email),
        )

        # Steps
        response = self.user_api_client.send_update_user_request(new_user)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.BAD_REQUEST),
            Conditions.body_field_equals("message", expected_message),
        )

    @allure.label("owner", "arrnel")
    @allure.story("Update user if user not exists")
    @allure.title(
        "[API] Update user should return 404_BAD_REQUEST "
        "when send update user request with not existing email"
    )
    def test_not_update_user_when_user_not_exists(self):

        # Data
        user = DataGenerator.random_user()

        # Steps
        response = self.user_api_client.send_update_user_request(user)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.NOT_FOUND),
            Conditions.body_field_equals("message", ACCOUNT_NOT_FOUND_MESSAGE),
        )
