import allure
import pytest

from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.page_scroller_component_test
@allure.feature("Page Scroller Component")
class TestPageScrollerComponent(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Page scroller")
    @allure.title("[WEB Component] Page scroller scroll page to top")
    def test_should_scroll_on_top_page(self):
        # Steps
        self.main_page.recommended_products.scroll_to_component()
        self.main_page.page_scroller.scroll_to_top()
        self.main_page.check_page_has_screenshot(
            "files/screenshot/page/main/main_page.png"
        )
