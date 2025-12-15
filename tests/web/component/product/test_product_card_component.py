import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.component
@allure.tag("component", "product_card", "animated_product_card")
@allure.epic("Web Component")
@allure.feature("[WEB] Product Card")
class TestProductCard(BaseWebTest):

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Card Component")
    @allure.title("[WEB Component] Product card should have expected data")
    def test_product_card_has_expected_data(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        card = self.main_page.recommended_products.get_card_by_title(product.title)

        # Assertions
        try:
            card.check_product_has_title(product.title)
        except AssertionError:
            pytest.xfail("TASK-1234")
        card.check_product_has_price(product.price)
        card.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/product_card/card.png",
        )

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Card Component")
    @allure.title("[WEB Component] Should add product to cart when click on add to cart button")
    def test_add_product_to_card_when_click_add_to_cart_button(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        self.main_page.recommended_products.get_card_by_title(product.title).add_to_cart()

        # Assertions
        self.main_page.notification.check_notification_has_success_added_product_message()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Card Component")
    @allure.title("[WEB Component] Should add product to cart when click on add to cart button from overlay")
    def test_add_product_to_card_when_click_overlay_add_to_cart_button(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        self.main_page.recommended_products.get_card_by_title(product.title).add_to_cart_from_overlay()

        # Assertions
        self.main_page.notification.check_notification_has_success_added_product_message()