import allure
import pytest

from src.config.config import CFG
from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.invoice_component_test
@pytest.mark.order_placed_page_test
@allure.feature("Place Order Component")
class TestPaymentComponent(BaseWebComponentTest):

    @pytest.mark.usefixtures(
        "open_payment_page",
        "auth_expected_user",
        "add_random_products_to_cart",
    )
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Payment Component")
    @allure.title("[WEB Component] Order placed page should have expected screenshot")
    def test_order_placed_page_should_have_expected_data(self):
        # Data
        card = DataGenerator.random_credit_card()

        # Step
        self.payment_page.payment_card_component.pay(card)

        # Assertion
        self.order_placed_page.check_page_has_screenshot(
            path_to_screenshot="files/screenshot/page/order_placed/order_placed_page.png",
        )

    @pytest.mark.download_file_test
    @pytest.mark.usefixtures("open_payment_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Payment Component")
    @allure.title("[WEB Component] Invoice should have expected price")
    def test_invoice_file_should_have_expected_price(
        self,
        auth_user,
        add_random_products_to_cart,
    ):
        # Data
        card = DataGenerator.random_credit_card()

        # Step
        self.payment_page.payment_card_component.pay(card)
        path_to_invoice = self.order_placed_page.download_invoice(
            "invoice.txt",
            retries=5,
            delay=2.0,
        )

        # Assertion
        self.order_placed_page.check_invoice_has_data(
            path_to_invoice,
            auth_user.name,
            add_random_products_to_cart.total_price,
        )

    @pytest.mark.download_file_test
    @pytest.mark.usefixtures("open_payment_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Payment Component")
    @allure.title("[WEB Component] Can download invoice multiple times")
    def test_can_download_invoice_multiple_times(
        self,
        auth_user,
        add_random_products_to_cart,
    ):
        # Data
        card = DataGenerator.random_credit_card()
        file_name_with_suffix = (
            "invoice (1).txt" if CFG.browser_name == "chrome" else "invoice(1).txt"
        )

        # Step
        self.payment_page.payment_card_component.pay(card)
        path_to_invoice1 = self.order_placed_page.download_invoice(
            "invoice.txt",
            retries=5,
            delay=2.0,
        )
        path_to_invoice2 = self.order_placed_page.download_invoice(
            file_name_with_suffix,
            retries=5,
            delay=2.0,
        )

        # Assertion
        self.order_placed_page.check_invoice_has_data(
            path_to_invoice1,
            auth_user.name,
            add_random_products_to_cart.total_price,
        )
        self.order_placed_page.check_invoice_has_data(
            path_to_invoice2,
            auth_user.name,
            add_random_products_to_cart.total_price,
        )
