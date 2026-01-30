from http import HTTPStatus

import allure
import pytest

from src.client.core.condition.conditions import Conditions
from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType
from tests.api.base_api_test import BaseApiTest


@pytest.mark.auth_test
@pytest.mark.component_test
@allure.feature("Auth")
class TestAuthApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Get csrf")
    @allure.title(
        "[API] Get csrf should return 200_OK "
        "when send get csrf request and contains csrf cookie"
    )
    def test_csrf(self):
        response = self.auth_api_client.send_get_csrf_token_request()
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.content_type(ContentType.HTML),
            Conditions.cookies_exists(CFG.csrf_cookie_title),
        )

    @allure.label("owner", "arrnel")
    @allure.story("Login with valid data")
    @allure.title(
        "[API] Login should return 200_OK "
        "when send login request with valid data and contains csrf cookie"
    )
    def test_login(self):

        # Steps
        csrf = (
            self.auth_api_client.send_get_csrf_token_request()
            .extract()
            .cookie(CFG.csrf_cookie_title)
        )
        login_response = self.auth_api_client.send_login_request(
            email="ar@ar.ar", password="1234567", csrf=csrf
        )

        # Assertions
        login_response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.content_type(ContentType.HTML),
            Conditions.cookies_exists(CFG.csrf_cookie_title),
        )
