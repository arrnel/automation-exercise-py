import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.component_test
@pytest.mark.filter_test
@pytest.mark.review_component_test
@allure.epic("Web Component")
@allure.feature("[WEB] Review Component")
class TestPaymentComponent(BaseWebTest):

    @pytest.mark.usefixtures(
        "open_payment_page", "auth_user", "add_random_products_to_cart"
    )
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Payment Component")
    @allure.title("[WEB Component] Payment component should have expected screenshot")
    def test_payment_card_component_has_expected_screenshot(self):
        # Assertions
        self.payment_page.payment_card_component.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/payment/empty_payment_card.png",
        )

    @pytest.mark.usefixtures(
        "open_payment_page", "auth_user", "add_random_products_to_cart"
    )
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Payment Component")
    @allure.title("[WEB Component] Payment component should have success status")
    def test_success_payment(self):
        # Data
        card = DataGenerator.random_credit_card()

        # Step & Assertion
        self.payment_page.payment_card_component.pay_and_check_payment_success(card)
