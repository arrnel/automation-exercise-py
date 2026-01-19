import allure
import pytest

from src.model.card import CardInfo
from tests.web.base_test import BaseWebTest


@pytest.mark.component_test
@pytest.mark.address_component_test
@pytest.mark.checkout_page_test
@allure.tag("component_test", "product_card", "animated_product_card")
@allure.epic("Web Component")
@allure.feature("[WEB] Address Component")
class TestProductItem(BaseWebTest):

    @pytest.mark.usefixtures(
        "open_checkout_page", "auth_user", "add_random_products_to_cart"
    )
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Billing Address Component")
    @allure.title("[WEB Component] Billing address has expected data")
    def test_billing_address_has_expected_data(self, card: CardInfo):

        # Component
        payment_card = self.payment_page.payment_card_component

        # Steps
        self.checkout_page.place_order()
        payment_card.pay(card)

        # Assertions
        payment_card.check_payment_successful()
        payment_card.check_component_has_screenshot(path_to_screenshot="")
