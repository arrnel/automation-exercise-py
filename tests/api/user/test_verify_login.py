from http import HTTPStatus

import allure
import pytest

from src.client.core.condition.conditions import Conditions
from src.model.user import User
from src.util.test.data_generator import DataGenerator
from tests.api.base_api_test import BaseApiTest

USER_EXISTS_MESSAGE = "User exists!"
USER_NOT_FOUND = "User not found!"


@pytest.mark.verify_login_test
@allure.feature("Verify Login")
class TestVerifyLoginApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Verify login with valid data")
    @allure.title("Should return user exists when user exists with email and password")
    def test_verify_login_with_credentials(self, create_user: User):

        # Steps
        response = self.verify_login_api_client.send_verify_login_request(
            create_user.email,
            create_user.password,
        )

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            Conditions.body_field_equals("message", USER_EXISTS_MESSAGE),
        )

    @allure.label("owner", "arrnel")
    @allure.story("Verify login with invalid data")
    @allure.title("Should return user not found when user password invalid")
    def test_verify_login_with_invalid_password(self, create_user: User):

        # Steps
        response = self.verify_login_api_client.send_verify_login_request(
            create_user.email,
            DataGenerator.random_password(),
        )

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.NOT_FOUND),
            Conditions.body_field_equals("message", USER_NOT_FOUND),
        )
