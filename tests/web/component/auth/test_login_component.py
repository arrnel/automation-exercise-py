import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.auth_test
@pytest.mark.login_page_test
@allure.feature("Sign In Component")
class TestLoginWeb(BaseWebComponentTest):

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.story("Sign in with valid credentials")
    @allure.title("[WEB] Sign in with valid data")
    def test_should_sign_in_with_valid_credentials(self, create_user):
        # Data
        user = create_user

        # Steps
        self.login_page.login_component.login(user.email, user.password)

        # Assertions
        self.login_page.check_page_is_not_visible()
        self.login_page.header.check_user_is_logged_in_as(user.name)

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.story("Sign in with invalid credentials")
    @allure.title("[WEB] Sign in with invalid credentials. Case: {case_title}")
    def test_should_not_sign_in_with_invalid_credentials(self, create_user):
        # Data
        user = create_user

        # Steps
        self.login_page.login_component.login(
            user.email, DataGenerator.random_password()
        )

        # Assertions
        self.login_page.login_component.check_login_error_has_message(
            "Your email or password is incorrect!"
        )
