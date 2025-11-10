import allure
import pytest

from tests.web.base_test import BaseWebTest


@pytest.mark.web_test
@allure.epic("UI")
@allure.feature("Component")
@allure.story("Notification")
class NotificationComponentTest(BaseWebTest):

    ##########################
    # ADD TO CARD NOTIFICATION
    ##########################
    def test_add_to_cart_notification_close_when_press_close_button(self, created_user_by_ui):
        # Data
        product = self.data_generator.get_random_product()

        # Steps
        self.main_page.products.get_card_by_title(product.title).add_product_to_cart()
        self.main_page.notification.close()

        # Assertions
        self.main_page.notification.check_component_is_not_exists()

    @pytest.mark.screenshot_test
    def test_add_product_to_cart_notification_has_expected_data_and_screenshot(self):
        # Data
        product = self.data_generator.get_random_product()

        # Steps
        self.main_page.products.add_product_to_cart(product.title)
        self.main_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()

        # Assertions
        self.cart_page.notification.check_notification_has_title()
        self.cart_page.notification.check_notification_has_description()
        self.cart_page.notification.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/notification/add_product_to_cart.png"
        )

    ################################################
    # PLACE ORDER WITHOUT AUTHORIZATION NOTIFICATION
    ################################################
    def test_place_order_without_authorization_notification_redirect_to_login_page_when_click_on_proceed_to_checkout(self):
        # Data
        product = self.data_generator.get_random_product()

        # Steps
        self.main_page.products.add_product_to_cart(product.title)
        self.main_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.cart_page.notification.close()

        # Assertion
        self.cart_page.notification.check_component_is_not_exists()
        self.login_page.check_page_is_visible()

    @pytest.mark.screenshot_test
    def test_place_order_without_authorization_notification_has_expected_data_and_screenshot(self):
        # Data
        product = self.data_generator.get_random_product()

        # Steps
        self.main_page.products.add_product_to_cart(product.title)
        self.main_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()

        # Assertions
        self.cart_page.notification.check_notification_has_title()
        self.cart_page.notification.check_notification_has_description()
        self.cart_page.notification.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/notification/proceed_to_checkout_wo_auth.png"
        )
