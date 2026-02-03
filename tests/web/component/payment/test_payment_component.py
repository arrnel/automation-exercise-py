import allure
import pytest

from src.model.card import CardInfo
from src.util.decorator.disabled_by_issue import disabled_by_issue
from tests.data_provider.card_data_provider import CardDataProviderUI
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.payment_component_test
@pytest.mark.payment_page_test
@allure.feature("Payment Component")
class TestPaymentComponent(BaseWebComponentTest):

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
    @allure.title(
        "[WEB Component] Pay with valid card should show success status message. Case: {case_title}"
    )
    @pytest.mark.parametrize(
        "case_title, card",
        CardDataProviderUI.valid_cards(),
        ids=[param[0] for param in CardDataProviderUI.valid_cards()],
    )
    def test_payment_with_valid_card(self, case_title: str, card: CardInfo):
        # Step & Assertion
        self.payment_page.payment_card_component.pay_and_check_payment_success(card)

    @disabled_by_issue(issue_id=4, reason="Missing card data validation")
    @pytest.mark.usefixtures(
        "open_payment_page", "auth_user", "add_random_products_to_cart"
    )
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Payment Component")
    @allure.title(
        "[WEB Component] Pay with invalid card should show error message. Case: {case_title}"
    )
    @pytest.mark.parametrize(
        "case_title, card",
        CardDataProviderUI.invalid_cards(),
        ids=[param[0] for param in CardDataProviderUI.invalid_cards()],
    )
    def test_payment_with_invalid_card(self, case_title: str, card: CardInfo):
        # Step
        self.payment_page.payment_card_component.pay(card)

        # Assertion
        self.order_placed_page.check_page_is_not_visible()
