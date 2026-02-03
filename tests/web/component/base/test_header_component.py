import allure
import pytest

from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.header_component_test
@allure.feature("Header Component")
class TestHeaderComponent(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title("[WEB Component] Header has expected screenshot")
    def test_header_has_expected_screenshot_when_not_authorized(self):
        # Assertions
        self.main_page.header.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/header/not_authorized.png",
        )

    @pytest.mark.usefixtures("auth_expected_user")
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title("[WEB Component] Header has expected screenshot when authorized")
    def test_header_has_expected_screenshot_when_authorized(self):
        # Assertions
        self.main_page.header.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/header/authorized.png",
        )

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title(
        "[WEB Component] Should navigate to main page by click on header logo"
    )
    def test_navigate_to_main_page_from_logo(self):
        # Steps
        self.login_page.header.go_to_main_page_by_logo()

        # Assertions
        self.main_page.check_page_is_visible()

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title(
        "[WEB Component] Should navigate to main page by click on header logo"
    )
    def test_navigate_to_main_page_from_header_menu(self):
        # Steps
        self.login_page.header.go_to_main_page()

        # Assertions
        self.main_page.check_page_is_visible()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title(
        "[WEB Component] Should navigate to products page by click 'Products' button"
    )
    def test_navigate_to_products_page(self):
        # Steps
        self.main_page.header.go_to_products_page()

        # Assertions
        self.products_page.check_page_is_visible()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title("[WEB Component] Should navigate to cart page by click 'Cart' button")
    def test_navigate_to_cart_page(self):
        # Steps
        self.main_page.header.go_to_cart_page()

        # Assertions
        self.cart_page.check_cart_is_empty()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title(
        "[WEB Component] Should navigate to login page by click 'Signup / Login' button"
    )
    def test_navigate_to_login_page_if_not_authenticated(self):
        # Steps
        self.main_page.header.go_to_login_page()

        # Assertions
        self.login_page.check_page_is_visible()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title("[WEB Component] Should visible user name when authorized")
    def test_display_logout_button_and_username_after_login(self, auth_user):
        # Assertions
        self.main_page.header.check_user_is_logged_in_as(auth_user.name)

    @pytest.mark.usefixtures("auth_user")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title(
        "[WEB Component] Should delete user name by click on 'Delete Account' button"
    )
    def test_delete_account_and_redirect_to_deleted_page(self):
        # Steps
        self.main_page.header.delete_account()

        # Assertion
        self.account_deleted_page.check_title_and_message_have_expected_texts()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Header Component")
    @allure.title(
        "[WEB Component] Should navigate to contact us page by click on 'Contact us' button"
    )
    def test_navigate_to_contact_us_page(self):
        # Steps
        self.main_page.header.go_to_contact_us_page()

        # Assertions
        self.contact_us_page.check_page_is_visible()
