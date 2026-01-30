from http import HTTPStatus

import allure
import pytest

from src.client.core.condition.conditions import Conditions
from src.model.user import User
from src.util.decorator.disabled_by_issue import disabled_by_issue
from src.util.store.user_store import ThreadSafeUserStore
from tests.api.base_api_test import BaseApiTest
from tests.data_provider.user_data_provider import UserDataProviderApi

SUCCESSFUL_CREATE_MESSAGE = "User created!"
EMAIL_ALREADY_EXIST_MESSAGE = "Email already exists!"


@pytest.mark.user_test
@allure.feature("User")
class TestCreateUserApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Create user with valid data")
    @pytest.mark.parametrize(
        "case_title, user",
        UserDataProviderApi.valid_sensitive_data_provider(),
        ids=[param[0] for param in UserDataProviderApi.valid_sensitive_data_provider()],
    )
    @allure.title(
        "[API] Create user should return 200_OK "
        "when send create user request with valid data. "
        "Case: {case_title}"
    )
    # @allure.title("Should create user with valid data. Case: {case_title}")
    def test_create_user_with_valid_data(self, case_title: str, user: User):

        # Precondition
        ThreadSafeUserStore().add_user(user)

        # Steps
        response = self.user_api_client.send_create_new_user_request(user)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.CREATED),
            Conditions.body_field_equals("message", SUCCESSFUL_CREATE_MESSAGE),
        )

    @disabled_by_issue(issue_id=1, reason="[WEB] Not validate sensitive data")
    @allure.label("owner", "arrnel")
    @allure.story("Create user with invalid data")
    @pytest.mark.parametrize(
        "case_title, user, message_error",
        UserDataProviderApi.invalid_sensitive_data_provider(),
        ids=[
            param[0] for param in UserDataProviderApi.invalid_sensitive_data_provider()
        ],
    )
    @allure.title(
        "[API] Create user should return 400_BAD_REQUEST "
        "when send create user request with invalid data. "
        "Case: {case_title}"
    )
    def test_not_create_user_with_invalid_data(
        self,
        case_title: str,
        user: User,
        message_error: str,
    ):

        # Precondition
        ThreadSafeUserStore().add_user(user)  # cause creates users with invalid data

        # Steps
        response = self.user_api_client.send_create_new_user_request(user)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.BAD_REQUEST),
            Conditions.body_field_equals("message", message_error),
        )

    @allure.label("owner", "arrnel")
    @allure.story("Create user with existing email")
    @allure.title(
        "[API] Create user should return 400_BAD_REQUEST "
        "when send create user request with existing email"
    )
    def test_not_create_user_with_exists_email(self, create_user):

        # Steps
        response = self.user_api_client.send_create_new_user_request(create_user)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.BAD_REQUEST),
            Conditions.body_field_equals("message", EMAIL_ALREADY_EXIST_MESSAGE),
        )
