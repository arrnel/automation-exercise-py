import allure
import pytest

from src.model.enum.user_type import UserType
from src.util.test.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.component
@pytest.mark.brand_filter
@allure.tag("component", "filter", "category_filter")
@allure.epic("Web Component")
@allure.feature("[WEB] Category Filter")
class TestCategoryFilter(BaseWebTest):

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title("[WEB Component] Category filter should have expected screenshot when collapsed")
    def test_category_filter_should_have_screenshot(self):
        # Steps
        self.main_page.navigate()

        # Assertion
        self.main_page.brand_filter.check_component_has_screenshot(
            "files/screenshot/component/filter/category/collapsed.png"
        )

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title("[WEB Component] Category filter should have expected screenshot when fully expanded")
    def test_category_filter_should_have_screenshot_when_expanded(self):
        # Component
        category_filter = self.main_page.category_filter

        # Data
        categories_groups = [
            user_type.value
            for user_type in [UserType.WOMEN, UserType.MEN, UserType.KIDS]
        ]

        # Steps
        self.main_page.navigate()
        category_filter.expand_groups(*categories_groups)

        # Assertions
        self.main_page.category_filter.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/filter/category/expanded.png",
            timeout=1,
        )

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title("[WEB Component] Category filter should have expected screenshot when collapsed after expand")
    def test_category_filter_should_have_screenshot_when_collapsed_after_expand(self):
        # Component
        category_filter = self.main_page.category_filter

        # Data
        categories_groups = [
            user_type.value
            for user_type in [UserType.WOMEN, UserType.MEN, UserType.KIDS]
        ]

        # Steps
        self.main_page.navigate()
        category_filter.expand_groups(*categories_groups)
        category_filter.collapse_groups(*categories_groups)

        # Assertions
        self.main_page.category_filter.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/filter/category/collapsed.png",
            timeout=1,
        )

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title("[WEB Component] Category filter should have expected screenshot when fully expanded")
    def test_category_filter_filter_products_by_category_expand(self):
        # Data
        group, category = DataGenerator.random_user_type_and_category()
        product_titles = self.product_api_service.get_all_product_titles_by_category(group, category)

        # Steps
        self.main_page.navigate()
        self.main_page.category_filter.select_group_category(group.value, category)

        # Assertions
        self.main_page.products.check_has_products(*product_titles)
