import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.carousel_component_test
@pytest.mark.product_carousel_component_test
@pytest.mark.main_page_test
@allure.feature("Carousel Component (Products)")
class TestProductCarousel(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Products Carousel")
    @allure.title(
        "[WEB Component] Products Carousel should show previous image when scroll left"
    )
    def test_should_show_previous_products_when_scroll_left(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(2)
        recommended_products.previous()

        # Assertions
        recommended_products.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/product/slide_1.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.title(
        "[WEB Component] Products Carousel should show next products when scroll right"
    )
    def test_should_show_next_products_when_scroll_right(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(1)
        recommended_products.next()

        # Assertions
        recommended_products.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/product/slide_2.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.title(
        "[WEB Component] Products Carousel should last products when scroll left on first slide"
    )
    def test_should_show_last_products_when_scroll_left_on_first_slide(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(1)
        recommended_products.previous()

        # Assertions
        recommended_products.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/product/slide_2.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.title(
        "[WEB Component] Products Carousel should first products when scroll right on last image"
    )
    def test_should_show_first_products_when_scroll_right_on_last_slide(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(2)
        recommended_products.next()

        # Assertions
        recommended_products.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/product/slide_1.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Products Carousel")
    @allure.title("[WEB Component] Add product to cart from product carousel")
    def test_add_product_to_cart(self):
        # Data
        product_title = DataGenerator.recommended_product().title

        # Steps
        self.main_page.recommended_products.add_product_to_cart(product_title)
        self.main_page.notification.close()
        self.main_page.header.go_to_cart_page()

        # Assertions
        self.cart_page.products.check_contains_product_titles(product_title)

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Products Carousel")
    @allure.title("[WEB Component] Product carousel should have expected product")
    def test_should_contains_expected_product(self):
        # Data
        product_title = DataGenerator.expected_product().title

        # Steps
        self.main_page.recommended_products.scroll_to_component()

        # Assertions
        self.main_page.recommended_products.check_contains_product(product_title)
