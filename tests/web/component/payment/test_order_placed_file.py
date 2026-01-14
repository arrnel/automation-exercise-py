import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.component_test
@pytest.mark.filter_test
@pytest.mark.review_component_test
@allure.epic("Web Component")
@allure.feature("[WEB] Place Order Component")
class TestPaymentComponent(BaseWebTest):

    @pytest.mark.usefixtures(
        "open_payment_page",
        "auth_user",
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
        self.order_placed_page.download_invoice()

        # Assertion
        self.order_placed_page.check_invoice_has_data(
            auth_user.name,
            add_random_products_to_cart.total_price,
        )

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

        # Step
        self.payment_page.payment_card_component.pay(card)
        self.order_placed_page.download_invoice()
        self.order_placed_page.download_invoice()

        # Assertion
        self.order_placed_page.check_invoice_has_data(
            auth_user.name,
            add_random_products_to_cart.total_price,
        )
        self.order_placed_page.check_invoice_has_data(
            auth_user.name,
            add_random_products_to_cart.total_price,
            "invoice(1).txt",
        )
