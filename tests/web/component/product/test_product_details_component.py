import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.product_test
@pytest.mark.product_details_component_test
@allure.feature("Product Details Component")
class TestProductCard(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Details Component")
    @allure.title("[WEB Component] Product details should have expected data")
    def test_product_details_has_expected_screenshot(self):
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
    @allure.title(
        "[WEB Component] Should add product to cart when click on add to cart button multiple times"
    )
    def test_add_product_to_card_when_click_add_to_cart_button(self):
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
    @allure.title(
        "[WEB Component] Should add product to cart when click on add to cart button"
    )
    def test_add_positive_products_count_to_card_when_set_positive_products_quantity_and_click_add_to_cart_button(
        self,
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
    @allure.title(
        "[WEB Component] Should not add negative products count to cart when click on add to cart button"
    )
    def test_add_negative_products_count_to_card_when_set_negative_products_quantity_and_click_add_to_cart_button(
        self,
    ):
        # Data
        product = DataGenerator.random_product()
        count = -1

        # Steps
        self.main_page.products.get_card_by_title(product.title).open()
        self.product_page.product_details.add_products_to_cart(count)

        # Assertions
        self.main_page.notification.check_component_is_not_visible()
