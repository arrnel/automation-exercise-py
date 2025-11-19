import allure
import pytest

from src.util.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.header
@pytest.mark.component
@allure.tag("component", "header")
@allure.epic("Web Component")
@allure.feature("[API] Create Users")
@allure.title("Test Create Users")
class TestHeaderComponent(BaseWebTest):

    def test_navigate_to_main_page_from_logo(self, browser_open):
        # Steps
        self.login_page.navigate()
        self.login_page.header.go_to_main_page_by_logo()

        # Assertions
        self.main_page.check_page_is_visible()

    def test_navigate_to_main_page_from_header_menu(self, browser_open):
        # Steps
        self.login_page.navigate()
        self.login_page.header.go_to_main_page()

        # Assertions
        self.main_page.check_page_is_visible()

    def test_navigate_to_products_page(self, browser_open):
        # Steps
        self.main_page.header.go_to_products_page()

        # Assertions
        self.products_page.check_page_is_visible()

    def test_navigate_to_cart_page(self, browser_open):
        # Steps
        self.main_page.header.go_to_cart_page()

        # Assertions
        self.cart_page.check_cart_is_empty()

    def test_navigate_to_login_page_if_not_authenticated(self, browser_open):
        # Steps
        self.main_page.header.go_to_login_page()

        # Assertions
        self.login_page.check_page_is_visible()

    def test_display_logout_button_and_username_after_login(self, browser_open):
        # Data
        user = DataGenerator.generate_user()

        # Steps
        self.login_page.sign_up_component.sign_up(user.name, user.email)
        self.sign_up_page.sign_up_component.send_user_data(user)
        self.main_page.navigate()

        # Assertions
        self.main_page.header.check_user_is_logged_in_as(user.name)

    def test_delete_account_and_redirect_to_deleted_page(self, browser_open):
        # Data
        user = DataGenerator.generate_user()

        # Steps
        self.login_page.sign_up_component.sign_up(user.name, user.email)
        self.sign_up_page.sign_up_component.send_user_data(user)
        self.account_created_page.submit()
        self.main_page.header.delete_account()

        # Assertion
        self.account_deleted_page.check_title_and_message_have_expected_texts()

    def test_navigate_to_contact_us_page(self, browser_open):
        # Steps
        self.login_page.header.go_to_contact_us_page()

        # Assertions
        self.contact_us_page.check_page_is_visible()
