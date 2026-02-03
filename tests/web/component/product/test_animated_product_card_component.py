import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.product_test
@pytest.mark.product_card_component_test
@pytest.mark.animated_product_card_component_test
@allure.feature("Product Card Component (Animated)")
class TestAnimatedProductCard(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Animated Product Card Component")
    @allure.title("[WEB Component] Animated product card should have expected data")
    def test_product_card_has_expected_data(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        card = self.main_page.products.get_card_by_title(product.title)

        # Assertions
        card.check_product_has_price(product.price)
        card.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/product_card/animated_card.png",
            timeout=0.1,
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Animated Product Card Component")
    @allure.title(
        "[WEB Component] Animated product card overlay should have expected data"
    )
    def test_product_card_overlay_has_expected_data(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        card = self.main_page.products.get_card_by_title(product.title)
        card.show_overlay()

        # Assertions
        card.check_product_has_price_in_overlay(product.price)
        card.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/product_card/animated_card_overlay.png",
            hover=True,
            timeout=1,
        )

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Animated Product Card Component")
    @allure.title(
        "[WEB Component] Should add product to cart when click on add to cart button"
    )
    def test_add_product_to_card_by_add_to_cart_button(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        self.main_page.products.get_card_by_title(product.title).add_to_cart()

        # Assertions
        self.main_page.notification.check_notification_has_success_added_product_message()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Animated Product Card Component")
    @allure.title(
        "[WEB Component] Should add product to cart when click on add to cart button from overlay"
    )
    def test_add_product_to_card_by_overlay_add_to_cart_button(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        self.main_page.products.get_card_by_title(
            product.title
        ).add_to_cart_from_overlay()

        # Assertions
        self.main_page.notification.check_notification_has_success_added_product_message()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Animated Product Card Component")
    @allure.title(
        "[WEB Component] Should open product page when click on view product button"
    )
    def test_open_product_page_when_click_on_view_product_button(self):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        self.main_page.products.get_card_by_title(product.title).open()

        # Assertions
        self.product_page.check_page_is_visible()
