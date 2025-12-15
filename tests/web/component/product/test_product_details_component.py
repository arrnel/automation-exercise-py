import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.component
@allure.tag("component", "product_details")
@allure.epic("Web Component")
@allure.feature("[WEB] Product Details")
class TestProductCard(BaseWebTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Details Component")
    @allure.title("[WEB Component] Product details should have expected data")
    def test_product_details_has_expected_screenshot(self, browser_open_main_page):
        # Data
        product = DataGenerator.expected_product()

        # Steps
        self.main_page.products.get_card_by_title(product.title).open()

        # Assertions
        product_details = self.product_page.product_details
        product_details.check_product_has_data(product)
        product_details.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/product_details/card.png",
        )

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Details Component")
    @allure.title("[WEB Component] Should add product to cart when click on add to cart button multiple times")
    def test_add_product_to_card_when_click_add_to_cart_button(self, browser_open_main_page):
        # Components
        product_details = self.product_page.product_details
        notification = self.product_page.notification

        # Data
        product = DataGenerator.random_product()

        # Steps
        self.main_page.products.get_card_by_title(product.title).open()
        product_details.add_to_cart()
        notification.close()
        product_details.add_to_cart()

        # Assertions
        self.main_page.notification.check_notification_has_success_added_product_message()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Details Component")
    @allure.title("[WEB Component] Should add product to cart when click on add to cart button")
    def test_add_positive_products_count_to_card_when_set_positive_products_quantity_and_click_add_to_cart_button(
            self,
            browser_open_main_page
    ):
        # Data
        product = DataGenerator.random_product()
        count = DataGenerator.random_quantity()

        # Steps
        self.main_page.products.get_card_by_title(product.title).open()
        self.product_page.product_details.add_products_to_cart(count)

        # Assertions
        self.main_page.notification.check_notification_has_success_added_product_message()

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Details Component")
    @allure.title("[WEB Component] Should add product to cart when click on add to cart button")
    def test_add_negative_products_count_to_card_when_set_negative_products_quantity_and_click_add_to_cart_button(
            self,
            browser_open_main_page
    ):
        # Data
        product = DataGenerator.random_product()
        count = DataGenerator.random_negative_int()

        # Steps
        self.main_page.products.get_card_by_title(product.title).open()
        self.product_page.product_details.add_products_to_cart(count)

        # Assertions
        self.main_page.notification.check_notification_is_not_success_added_product_message()
