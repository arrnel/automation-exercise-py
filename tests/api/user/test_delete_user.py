from http import HTTPStatus

import allure
import pytest

from src.client.core.condition.conditions import Conditions
from src.util.test.data_generator import DataGenerator
from tests.api.base_api_test import BaseApiTest

ACCOUNT_NOT_FOUND_MESSAGE = "Account not found!"
SUCCESSFUL_DELETE_MESSAGE = "Account deleted!"


@pytest.mark.user_test
@allure.feature("User")
class TestDeleteUserApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Delete user if user exists")
    @allure.title(
        "[API] Delete user should return 200_OK "
        "when send delete user request and user exists"
    )
    def test_delete_user_when_user_exists(self, create_user):

        # Steps
        response = self.user_api_client.send_delete_user_request(
            create_user.email,
            create_user.password,
        )

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            Conditions.body_field_equals("message", SUCCESSFUL_DELETE_MESSAGE),
        )

    @allure.label("owner", "arrnel")
    @allure.story("Delete user if user not exists")
    @allure.title(
        "[API] Delete user should return 404_NOT_FOUND "
        "when send delete user request and user not exists"
    )
    def test_not_delete_user_when_user_not_exists(self):

        # Steps
        response = self.user_api_client.send_delete_user_request(
            DataGenerator.random_email(), DataGenerator.random_password()
        )

        # Assertion
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.NOT_FOUND),
            Conditions.body_field_equals("message", ACCOUNT_NOT_FOUND_MESSAGE),
        )
