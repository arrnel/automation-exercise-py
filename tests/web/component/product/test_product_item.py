import random
from random import choice

import allure
import pytest

from src.model.product_item_info import ProductItemInfo
from src.util import collection_util
from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.product_test
@pytest.mark.product_item_component_test
@allure.feature("Product Item Component")
class TestProductItem(BaseWebComponentTest):

    @pytest.mark.usefixtures("open_cart_page", "auth_user")
    @pytest.mark.screenshot_test
    @pytest.mark.cart_page_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Product item should have expected data")
    def test_product_item_has_expected_data(self, add_expected_products_to_cart):
        # Component
        products = self.cart_page.products

        # Data
        product_title = DataGenerator.expected_product().title

        # Assertions
        products.check_contains_exact_product_items(add_expected_products_to_cart)
        products.get_item_by_title(product_title).check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/product_item/removable_item.png",
            timeout=0.5,
        )

    @pytest.mark.usefixtures(
        "open_cart_page",
        "auth_user",
        "add_expected_product_to_cart",
    )
    @pytest.mark.cart_page_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title(
        "[WEB Component] Product item should navigate to product page when click on item title"
    )
    def test_product_item_title_navigate_to_product_page(self):
        # Data
        title = DataGenerator.expected_product().title

        # Steps
        self.cart_page.products.get_item_by_title(title).navigate_to_product()

        # Assertions
        self.product_page.product_details.check_product_has_title(title)

    @pytest.mark.usefixtures("open_cart_page", "auth_user")
    @pytest.mark.cart_page_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should increase product item quantity")
    def test_increase_product_item_quantity_when_add_product_to_cart(
        self,
        add_random_products_to_cart,
    ):
        # Data
        quantity = DataGenerator.random_quantity()
        product = random.choice(add_random_products_to_cart.products_info)
        add_random_products_to_cart.update_product_quantity_by_title(
            product.title, product.quantity + quantity
        )

        # Steps
        self.cart_page.products.get_item_by_title(product.title).navigate_to_product()
        self.product_page.product_details.add_products_to_cart(quantity)
        self.product_page.notification.close()
        self.main_page.header.go_to_cart_page()

        # Assertions
        self.cart_page.products.check_contains_exact_product_items(
            add_random_products_to_cart
        )

    @pytest.mark.usefixtures("auth_user", "open_cart_page")
    @pytest.mark.checkout_page_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should remove product from cart")
    def test_product_item_not_exists_when_click_remove_product_item_button(
        self,
        add_expected_products_to_cart,
    ):
        # Component
        cart_products = self.cart_page.products

        # Data
        random_expected_products = collection_util.get_random_unique_values(
            add_expected_products_to_cart.products_info,
            count=2,
        )
        removed_product_title = random_expected_products[0].title
        exists_product_title = random_expected_products[1].title

        # Steps
        cart_products.get_item_by_title(removed_product_title).remove()

        # Assertions
        cart_products.check_contains_product_titles(exists_product_title)
        cart_products.check_not_contains_product_titles(removed_product_title)

    @pytest.mark.usefixtures("auth_user", "open_checkout_page")
    @pytest.mark.checkout_page_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should have all products expected total price")
    def test_all_products_total_price(self, add_random_products_to_cart):
        # Assertions
        self.checkout_page.products.check_all_products_total_price(
            add_random_products_to_cart.total_price
        )

    @pytest.mark.usefixtures("auth_user", "open_checkout_page")
    @pytest.mark.checkout_page_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should increase all products total price")
    def test_increase_all_products_total_price_when_add_product(
        self,
        add_random_products_to_cart,
    ):
        # Data
        product_items_info = add_random_products_to_cart
        quantity = DataGenerator.random_quantity()
        product = DataGenerator.random_product()
        product_items_info.add_product_items(
            [ProductItemInfo.from_product(product, quantity)]
        )

        # Steps
        self.product_page.navigate(product.id)
        self.product_page.product_details.add_products_to_cart(quantity)
        self.checkout_page.navigate()

        # Assertions
        self.checkout_page.products.check_all_products_total_price(
            product_items_info.total_price
        )

    @pytest.mark.usefixtures("auth_user", "open_cart_page")
    @pytest.mark.checkout_page_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Product Item Component")
    @allure.title("[WEB Component] Should decrease all products total price")
    def test_decrease_all_products_total_price_when_remove_product(
        self,
        add_random_products_to_cart,
    ):

        # Data
        product_items_info = add_random_products_to_cart
        product = choice(product_items_info.products_info)
        product_items_info.remove_by_ids(product.id)

        # Steps
        self.cart_page.products.get_item_by_title(product.title).remove()
        self.cart_page.proceed_to_checkout()

        # Assertions
        self.checkout_page.products.check_all_products_total_price(
            product_items_info.total_price
        )
