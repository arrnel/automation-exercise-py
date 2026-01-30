import allure
import pytest

from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.address_component_test
@pytest.mark.checkout_page_test
@allure.feature("Address Component")
class TestAddressComponent(BaseWebComponentTest):

    @pytest.mark.usefixtures(
        "auth_expected_user",
        "add_random_products_to_cart",
        "open_checkout_page",
    )
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Billing Address Component")
    @allure.title("[WEB Component] Billing address has expected data")
    def test_billing_address_has_expected_data(self):
        # Assertions
        self.checkout_page.billing_address_component.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/address/billing_address.png"
        )

    @pytest.mark.usefixtures(
        "auth_expected_user",
        "add_random_products_to_cart",
        "open_checkout_page",
    )
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Delivery Address Component")
    @allure.title("[WEB Component] Delivery address has expected data")
    def test_delivery_address_has_expected_data(self):
        # Assertions
        self.checkout_page.delivery_address_component.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/address/delivery_address.png"
        )
