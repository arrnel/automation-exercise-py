import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.login
@allure.tag("auth")
@allure.epic("Auth")
@allure.feature("[WEB] Sign in")
class TestLoginWeb(BaseWebTest):

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.story("Sign in with valid credentials")
    @allure.title("[WEB] Sign in with valid data")
    def test_should_sign_in_with_valid_credentials(self, created_user_by_ui):
        # Data
        user = created_user_by_ui

        # Steps
        self.login_page.login_component.login(user.email, user.password)

        # Assertions
        self.login_page.check_page_is_not_visible()
        self.login_page.header.check_user_is_logged_in_as(user.name)

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.story("Sign in with invalid credentials")
    @allure.title("[WEB] Sign in with valid credentials. Case: {case_title}")
    def test_should_not_sign_in_with_invalid_credentials(self, created_user_by_ui):
        # Data
        user = created_user_by_ui

        # Steps
        self.login_page.login_component.login(
            user.email, DataGenerator.random_password()
        )

        # Assertions
        self.login_page.check_page_is_visible()
        self.login_page.header.check_user_is_not_authorized()
