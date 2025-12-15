from random import choice

import allure
import pytest

from src.mapper.product_mapper import ProductMapper
from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.component
@allure.tag("component", "product_card", "animated_product_card")
@allure.epic("Web Component")
@allure.feature("[WEB] Product Card")
class TestProductItem(BaseWebTest):

    @pytest.mark.usefixtures("open_cart_page", "add_expected_products_to_cart")
    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Product item should have expected data")
    def test_product_item_has_expected_data(self, add_expected_product_to_cart):
        # Data
        product_item = add_expected_product_to_cart.products_info[0]

        # Assertions
        self.cart_page.products.check_contains_exact_product_items(add_expected_product_to_cart)
        self.cart_page.products.get_item_by_title(product_item.title).check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/product_item/removable_item.png",
        )

    @pytest.mark.usefixtures("open_cart_page", "add_expected_product_to_cart")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Product item should navigate to product page when click on item title")
    def test_product_item_title_navigate_to_product_page(self):
        # Data
        title = DataGenerator.expected_product().title

        # Steps
        self.cart_page.products.get_item_by_title(title).navigate_to_product()

        # Assertions
        self.product_page.product_details.check_product_has_title(title)

    @pytest.mark.usefixtures("open_cart_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should increase product item quantity")
    def test_increase_product_item_quantity_when_add_product_to_cart(self, add_expected_products_to_cart):
        # Data
        quantity = DataGenerator.random_quantity()
        product_item_info = add_expected_products_to_cart
        product_title = product_item_info.products_info[0].title
        product_item_info.update_product_quantity_by_title(
            product_title,
            product_item_info.products_info[0].quantity + quantity
        )

        # Steps
        self.cart_page.products.get_item_by_title(product_title).navigate_to_product()
        self.product_page.product_details.add_products_to_cart(quantity)
        self.product_page.notification.close()
        self.main_page.header.go_to_cart_page()

        # Assertions
        self.cart_page.products.check_contains_exact_product_items(product_item_info)

    @pytest.mark.usefixtures("open_expected_product_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should remove product from cart")
    def test_product_item_not_exists_when_click_remove_product_item_button(self, add_expected_products_to_cart):
        # Component
        cart_products = self.cart_page.products

        # Data
        product_item_info = add_expected_products_to_cart
        removed_product_title = product_item_info.products_info[0].title
        exists_product_title = product_item_info.products_info[1].title

        # Steps
        cart_products.get_item_by_title(removed_product_title).remove()

        # Assertions
        cart_products.check_not_contains_product_titles(removed_product_title)
        cart_products.check_contains_product_titles(exists_product_title)

    @pytest.mark.usefixtures("auth_user", "open_checkout_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should have all products expected total price")
    def test_all_products_total_price(self, add_random_products_to_cart):
        # Assertions
        self.checkout_page.products.check_all_products_total_price(add_random_products_to_cart.total_price)

    @pytest.mark.usefixtures("auth_user", "open_checkout_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should increase all products total price")
    def test_increase_all_products_total_price_when_add_product(self, add_random_products_to_cart):
        # Data
        product_items_info = add_random_products_to_cart
        quantity = DataGenerator.random_quantity()
        product = DataGenerator.random_product()
        product_items_info.add_product_items([ProductMapper.to_product_item_info(product, quantity)])

        # Steps
        self.product_page.navigate(product.id).add_products_to_cart(quantity)
        self.checkout_page.navigate()

        # Assertions
        self.checkout_page.products.check_all_products_total_price(product_items_info.total_price)


    @pytest.mark.usefixtures("auth_user", "open_cart_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should decrease all products total price")
    def test_decrease_all_products_total_price_when_remove_product(self, add_random_products_to_cart):

        # Data
        product_items_info = add_random_products_to_cart
        product = choice(product_items_info.products_info)
        product_items_info.remove_by_ids(product.id)

        # Steps
        self.cart_page.products.get_item_by_title(product.title).remove()
        self.cart_page.proceed_to_checkout()

        # Assertions
        self.checkout_page.products.check_all_products_total_price(product_items_info.total_price)
