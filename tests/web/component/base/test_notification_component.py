import allure
import pytest

from tests.web.base_web_component_test import BaseWebComponentTest

ADDED_PRODUCT_NOTIFICATION_TITLE = "Added!"
ADDED_PRODUCT_NOTIFICATION_DESCRIPTION = "Your product has been added to cart."
PLACE_ORDER_WITHOUT_AUTH_NOTIFICATION_TITLE = "Checkout"
PLACE_ORDER_WITHOUT_AUTH_NOTIFICATION_DESCRIPTION = (
    "Register / Login account to proceed on checkout."
)


@pytest.mark.component_test
@pytest.mark.notification_component_test
@allure.feature("Notification Component")
class TestNotificationComponent(BaseWebComponentTest):

    ##########################
    # ADD TO CARD NOTIFICATION
    ##########################
    @pytest.mark.usefixtures("open_products_page")
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Add Product Notification")
    @allure.title(
        "[WEB Component] Add product notification should have expected data and screenshot"
    )
    def test_add_product_to_cart_notification_has_expected_data_and_screenshot(self):
        # Data
        product = self.data_generator.random_product()

        # Steps
        self.products_page.products.get_card_by_title(product.title).add_to_cart()

        # Assertions
        self.cart_page.notification.check_notification_has_title(
            ADDED_PRODUCT_NOTIFICATION_TITLE
        )
        self.cart_page.notification.check_notification_has_description(
            ADDED_PRODUCT_NOTIFICATION_DESCRIPTION
        )
        self.cart_page.notification.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/notification/add_product_to_cart.png"
        )

    @pytest.mark.usefixtures("open_products_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Add Product Notification")
    @allure.title(
        "[WEB Component] Add product notification should be closed when click on close button"
    )
    def test_add_to_cart_notification_close_when_press_close_button(self):
        # Data
        product = self.data_generator.random_product()

        # Steps
        self.products_page.products.get_card_by_title(product.title).add_to_cart()
        self.products_page.notification.close()

        # Assertions
        self.products_page.notification.check_component_is_not_visible()

    ################################################
    # PLACE ORDER WITHOUT AUTHORIZATION NOTIFICATION
    ################################################
    @pytest.mark.usefixtures("open_products_page")
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Place Order Without Authorization Notification")
    @allure.title(
        "[WEB Component] Place order without authorization notification "
        "should have expected data and screenshot"
    )
    def test_place_order_without_authorization_notification_has_expected_data_and_screenshot(
        self,
    ):
        # Data
        product = self.data_generator.random_product()

        # Steps
        self.products_page.products.get_card_by_title(product.title).add_to_cart()
        self.products_page.notification.close()
        self.products_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()

        # Assertions
        self.cart_page.notification.check_notification_has_title(
            PLACE_ORDER_WITHOUT_AUTH_NOTIFICATION_TITLE
        )
        self.cart_page.notification.check_notification_has_description(
            PLACE_ORDER_WITHOUT_AUTH_NOTIFICATION_DESCRIPTION
        )
        self.cart_page.notification.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/notification/proceed_without_auth.png"
        )

    @pytest.mark.usefixtures("open_products_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Place Order Without Authorization Notification")
    @allure.title(
        "[WEB Component] Place order without authorization notification proceed to checkout button "
        "should navigate to login page"
    )
    def test_place_order_without_authorization_notification_redirect_to_login_page_when_click_on_proceed_to_checkout(
        self,
    ):
        # Data
        product = self.data_generator.random_product()

        # Steps
        self.products_page.products.get_card_by_title(product.title).add_to_cart()
        self.products_page.notification.close()
        self.products_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.cart_page.notification.navigate()

        # Assertion
        self.cart_page.notification.check_component_is_not_visible()
        self.login_page.check_page_is_visible()
