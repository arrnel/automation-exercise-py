import allure
import pytest

from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.filter_test
@pytest.mark.search_filter_test
@pytest.mark.products_page_test
@allure.feature("Search Filter")
class TestSearchFilter(BaseWebComponentTest):

    @pytest.mark.usefixtures("open_products_page")
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Search Filter")
    @allure.title("[WEB Component] Search filter should have expected screenshot")
    def test_search_filter_should_have_screenshot(self):
        # Step & Assertion
        self.products_page.search_filter.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/filter/search/empty.png",
            timeout=1,
        )

    @pytest.mark.usefixtures("open_products_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Search Filter")
    @allure.title("[WEB Component] Search filter should filter products by query")
    def test_search_filter_filter_products_by_query(self):
        # Data
        query = "Top"
        products = self.product_api_service.search_product_titles(query)

        # Steps
        self.products_page.search_filter.search(query)

        # Assertions
        self.products_page.products.check_has_products(*products)

    @pytest.mark.usefixtures("open_products_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Search Filter")
    @allure.title(
        "[WEB Component] Search filter should return all products when filter by empty query"
    )
    def test_search_filter_returns_all_products_when_filter_by_empty_query(self):
        # Data
        query = ""
        products = self.product_api_service.get_all_product_titles()

        # Steps
        self.products_page.search_filter.search(query)

        # Assertions
        self.products_page.products.check_contains_products(*products)

    @pytest.mark.usefixtures("open_products_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Search Filter")
    @allure.title("[WEB Component] Search filter should return empty products catalog")
    def test_search_filter_returns_empty_catalog_when_(self):
        # Data
        query = DataGenerator.random_sentence()

        # Steps
        self.products_page.search_filter.search(query)

        # Assertions
        self.products_page.products.check_catalog_is_empty()
