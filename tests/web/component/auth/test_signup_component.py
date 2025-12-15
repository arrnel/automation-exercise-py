import allure
import pytest

from src.model.user import User
from src.util.api.user_store import ThreadSafeUserStore
from tests.data_provider.user_data_provider import UserDataProviderUI
from tests.web.base_test import BaseWebTest


@allure.tag("auth")
@allure.epic("Auth")
@allure.feature("[WEB] Sign up")
class TestSignUpWeb(BaseWebTest):

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.story("Sign up with valid credentials")
    @allure.title("[WEB] Sign up with valid data. Case: {case_title}")
    @pytest.mark.parametrize(
        "case_title,user",
        UserDataProviderUI.valid_sensitive_data_provider(),
        ids=[param[0] for param in UserDataProviderUI.valid_sensitive_data_provider()],
    )
    def test_should_sign_up_with_valid_data(self, case_title:str, user: User):
        # Data
        ThreadSafeUserStore().add_user(user)

        # Steps
        self.login_page.sign_up_component.sign_up(user.name, user.email)
        self.sign_up_page.sign_up_component.send_user_data(user)

        # Assertions
        self.account_created_page.check_page_is_visible()

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.story("Sign up with invalid credentials")
    @allure.title("[WEB] Sign up with valid data. Case: {case_title}")
    @pytest.mark.parametrize(
        "case_title,user",
        UserDataProviderUI.valid_sensitive_data_provider(),
        ids=[param[0] for param in UserDataProviderUI.valid_sensitive_data_provider()],
    )
    def test_should_not_sign_up_when_contains_invalid_data(self, case_title: str, user: User):

        # Data
        ThreadSafeUserStore().add_user(user)

        # Steps
        self.login_page.sign_up_component.sign_up(user.name, user.email)
        self.sign_up_page.sign_up_component.send_user_data(user)

        # Assertions
        self.sign_up_page.check_page_is_visible()
