import allure
import pytest

from src.model.enum.user_type import UserType
from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest

PERCENT_OF_TOLERANCE = 0.002


@pytest.mark.component_test
@pytest.mark.filter_test
@pytest.mark.category_filter_test
@pytest.mark.main_page_test
@pytest.mark.products_page_test
@allure.feature("Category Filter")
class TestCategoryFilter(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title(
        "[WEB Component] Category filter should have expected screenshot when collapsed"
    )
    def test_category_filter_should_have_screenshot(self):
        # Steps
        self.main_page.navigate()

        # Assertion
        self.main_page.category_filter.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/filter/category/collapsed.png",
            percent_of_tolerance=PERCENT_OF_TOLERANCE,
            timeout=0.1,
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title(
        "[WEB Component] Category filter should have expected screenshot when group expanded"
    )
    def test_category_filter_should_have_screenshot_when_group_expanded(self):
        # Component
        category_filter = self.main_page.category_filter

        # Data
        group = DataGenerator.random_user_type().value

        # Steps
        self.main_page.navigate()
        category_filter.expand_group(group)

        # Assertions
        self.main_page.category_filter.check_component_has_screenshot(
            path_to_screenshot=f"files/screenshot/component/filter/category/expanded_{group.lower()}.png",
            percent_of_tolerance=PERCENT_OF_TOLERANCE,
            timeout=0.1,
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title(
        "[WEB Component] Category filter group should be collapsed after collapse expanded group"
    )
    def test_category_filter_should_have_screenshot_when_collapse_expanded(self):
        # Component
        category_filter = self.main_page.category_filter

        # Data
        group1 = DataGenerator().random_user_type().value

        # Steps
        self.main_page.navigate()
        category_filter.expand_group(group1)
        category_filter.collapse_group(group1)

        # Assertions
        self.main_page.category_filter.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/filter/category/collapsed.png",
            percent_of_tolerance=PERCENT_OF_TOLERANCE,
            timeout=0.1,
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title(
        "[WEB Component] [WEB Component] Category filter group should be collapsed after expand another group"
    )
    def test_category_filter_should_have_screenshot_when_expand_collapse_expanded(self):
        # Component
        category_filter = self.main_page.category_filter

        # Data
        group1 = DataGenerator().random_user_type().value
        group2 = DataGenerator().random_user_type_except(UserType(group1)).value

        # Steps
        self.main_page.navigate()
        category_filter.expand_group(group1)
        category_filter.expand_group(group2)

        # Assertions
        self.main_page.category_filter.check_component_has_screenshot(
            path_to_screenshot=f"files/screenshot/component/filter/category/expanded_{group2.lower()}.png",
            percent_of_tolerance=PERCENT_OF_TOLERANCE,
            timeout=0.1,
        )

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Category Filter")
    @allure.title(
        "[WEB Component] Category filter should have expected screenshot when fully expanded"
    )
    def test_category_filter_filter_products_by_category_expand(self):
        # Data
        group, category = DataGenerator.random_user_type_and_category()
        product_titles = self.product_api_service.get_all_product_titles_by_category(
            group, category
        )

        # Steps
        self.main_page.navigate()
        self.main_page.category_filter.select_group_category(group.value, category)

        # Assertions
        self.main_page.products.check_has_products(*product_titles)
