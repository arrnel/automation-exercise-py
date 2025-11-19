import allure
import pytest

from tests.web.base_test import BaseWebTest


@pytest.mark.web_test
@allure.epic("UI")
@allure.feature("Component")
@allure.story("Page scroller")
class PageScrollerComponentTest(BaseWebTest):

    @pytest.mark.screenshot_test
    def test_should_scroll_on_top_page(self, browser_open):
        # Steps
        self.main_page.recommended_products.scroll_to_component()
        self.main_page.page_scroller.scroll_to_top()
        self.main_page.check_page_has_screenshot("files/screenshots/page/main_page.png")
