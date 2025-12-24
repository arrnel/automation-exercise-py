import allure
import pytest

from tests.web.base_test import BaseWebTest


@pytest.mark.component_test
@pytest.mark.filter_test
@pytest.mark.brand_filter_test
@allure.epic("Web Component")
@allure.feature("[WEB] Brand Filter")
class TestBrandFilter(BaseWebTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Brand Filter")
    @allure.title("[WEB Component] Brand filter should have expected screenshot")
    def test_brand_filter_should_have_screenshot(self):
        # Steps
        self.main_page.navigate()

        # Assertion
        self.main_page.brand_filter.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/filter/brand/brand_filter.png"
        )

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Brand Filter")
    @allure.title("[WEB Component] Brand filter should filters products by brand")
    def test_brand_filter_show_filtered_products_by_brand(self):
        # Data
        brand = self.data_generator.random_brand_title()
        brand_products = self.product_api_service.get_all_brand_product_titles(brand)

        # Steps
        self.main_page.navigate()

        # Assertion
        self.main_page.brand_filter.select(brand)
        self.products_page.products.check_has_products(*brand_products)
