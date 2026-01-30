from http import HTTPStatus

import allure
import pytest

from src.client.core.condition.conditions import Conditions
from src.util.test.data_generator import DataGenerator
from tests.api.base_api_test import BaseApiTest

ACCOUNT_NOT_FOUND_MESSAGE = "Account not found with this email, try another email!"


@pytest.mark.user_test
@allure.feature("User")
class TestGetUserApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Get user when user exists")
    @allure.title(
        "[API] Get user should return 200_OK when send get user request and user exists"
    )
    def test_get_user_when_user_exists(self, create_user):

        # Data
        user = create_user

        # Steps
        response = self.user_api_client.send_get_user_by_email_request(user.email)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            Conditions.body_field_not_equals("user.id", None, 0),
        )

    @allure.label("owner", "arrnel")
    @allure.story("Get user when user not exists")
    @allure.title(
        "[API] Get user should return 404_NOT_FOUND when send get user request and user not exists"
    )
    def test_get_user_return_not_found_when_user_not_exists(self):

        # Data
        email = DataGenerator.random_email()

        # Steps
        response = self.user_api_client.send_get_user_by_email_request(email)

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.NOT_FOUND),
            Conditions.body_field_equals("message", ACCOUNT_NOT_FOUND_MESSAGE),
        )
