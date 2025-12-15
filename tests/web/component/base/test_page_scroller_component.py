import allure
import pytest

from tests.web.base_test import BaseWebTest


@pytest.mark.web_test
@allure.epic("UI")
@allure.feature("Component")
@allure.story("Page scroller")
class PageScrollerComponentTest(BaseWebTest):

    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Page scroller")
    @allure.title("[WEB Component] Page scroller scroll page to top")
    def test_should_scroll_on_top_page(self):
        # Steps
        self.main_page.recommended_products.scroll_to_component()
        self.main_page.page_scroller.scroll_to_top()
        self.main_page.check_page_has_screenshot("files/screenshots/page/main_page.png")
