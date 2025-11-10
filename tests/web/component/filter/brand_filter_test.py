import pytest

from tests.web.base_test import BaseWebTest


@pytest.mark.web_test
class BrandFilterTest(BaseWebTest):

    @pytest.mark.screenshot_test
    def test_brand_filter_should_have_screenshot(self, browser_open):
        # Steps
        self.main_page.navigate()

        # Assertion
        self.main_page.brand_filter.check_component_has_screenshot("files/screenshot/component/filter/brand/brand_filter.png")

    def test_brand_filter_show_filtered_products_by_brand(self, browser_open):
        # TODO: add API to get filtered products and parser of titles
        # Data
        brand = self.data_generator.random_brand()
        # brand_products =
        brand_product_titles = [""]

        # Steps
        self.main_page.navigate()

        # Assertion
        self.main_page.brand_filter.select(brand)
        self.products_page.products.check_products_quantity(len(brand_product_titles))
        self.products_page.products.check_contains_products(brand_product_titles)
