import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@allure.tag("carousel_component", "image_carousel_component")
@allure.epic("[Web] Component - Image Carousel")
@allure.feature("[Web] Component - Image Carousel")
class TestProductCarousel(BaseWebTest):

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Products Carousel")
    @allure.title("[WEB Component] Products Carousel should show previous image when scroll left")
    def test_should_show_previous_products_when_scroll_left(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(2)
        recommended_products.next()

        # Assertions
        recommended_products.check_carousel_has_screenshot(
            "files/img/screenshot/component/carousel/product/recommended/3.png")

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Products Carousel")
    @allure.title("[WEB Component] Products Carousel should show next image when scroll right")
    def test_should_show_next_products_when_scroll_right(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(2)
        recommended_products.previous()

        # Assertions
        recommended_products.check_carousel_has_screenshot(
            "files/img/screenshot/component/carousel/product/recommended/1.png")

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Products Carousel")
    @allure.title("[WEB Component] Products Carousel should last image when scroll left on first image")
    def test_should_show_last_products_when_scroll_left_on_first_image(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(1)
        recommended_products.previous()

        # Assertions
        recommended_products.check_carousel_has_screenshot(
            "files/img/screenshot/component/carousel/product/recommended/3.png")

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Products Carousel")
    @allure.title("[WEB Component] Products Carousel should first image when scroll right on last image")
    def test_should_show_first_products_when_scroll_right_on_last_image(self):
        # Component
        recommended_products = self.main_page.recommended_products

        # Steps
        recommended_products.wait_until_slide_will_be_active(3)
        recommended_products.next()

        # Assertions
        recommended_products.check_carousel_has_screenshot(
            "files/img/screenshot/component/carousel/product/recommended/1.png",
        )

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
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

        # Assertions
        self.main_page.recommended_products.check_contains_product(product_title)
