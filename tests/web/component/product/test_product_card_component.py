import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.product_test
@pytest.mark.simple_product_card_component_test
@allure.feature("Product Card Component (Simple)")
class TestProductCard(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Card Component")
    @allure.title("[WEB Component] Product card should have expected data")
    def test_product_card_has_expected_data(self):

        # Component
        recommended_products = self.main_page.recommended_products

        # Data
        expected_product_title = "Winter Top"
        product_titles = DataGenerator.recommended_product_titles()
        product_card = recommended_products.get_card_by_title(expected_product_title)
        product = DataGenerator.product(expected_product_title)

        # Assertions
        product_card.check_product_has_title(product.title)
        product_card.check_product_has_price(product.price)
        product_card.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/product_card/card.png",
        )
        try:
            recommended_products.check_contains_products(*product_titles)
        except AssertionError:
            pytest.xfail("TASK-1234")

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Card Component")
    @allure.title(
        "[WEB Component] Should add product to cart when click on add to cart button"
    )
    def test_add_product_to_card_when_click_add_to_cart_button(self):

        # Components
        recommended_products = self.main_page.recommended_products

        # Data
        product_title = DataGenerator.recommended_product().title

        # Steps
        recommended_products.get_card_by_title(product_title).add_to_cart()

        # Assertions
        self.main_page.notification.check_notification_has_success_added_product_message()
