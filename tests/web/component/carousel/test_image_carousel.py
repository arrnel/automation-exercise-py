import allure
import pytest

from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.carousel_component_test
@pytest.mark.image_carousel_component_test
@pytest.mark.main_page_test
@allure.feature("Carousel Component (Images)")
class TestImageCarousel(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Image Carousel")
    @allure.title(
        "[WEB Component] Image Carousel should show previous image when scroll left"
    )
    def test_should_show_previous_image_when_scroll_left(self):

        # Component
        banner = self.main_page.banner

        # Steps
        banner.wait_until_slide_will_be_active(2)
        banner.previous()

        # Assertions
        banner.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/image/slide_1.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.title(
        "[WEB Component] Image Carousel should show next image when scroll right"
    )
    def test_should_show_next_image_when_scroll_right(self):

        # Component
        banner = self.main_page.banner

        # Steps
        banner.wait_until_slide_will_be_active(2)
        banner.next()

        # Assertions
        banner.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/image/slide_3.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.title(
        "[WEB Component] Image Carousel should show last image when scroll left on first image"
    )
    def test_should_show_last_image_when_scroll_left_on_first_image(self):

        # Component
        banner = self.main_page.banner

        # Steps
        banner.wait_until_slide_will_be_active(1)
        banner.previous()

        # Assertions
        banner.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/image/slide_3.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.title(
        "[WEB Component] Image Carousel should show first image when scroll right on last image"
    )
    def test_should_show_first_image_when_scroll_right_on_last_image(self):

        # Component
        banner = self.main_page.banner

        # Steps
        banner.wait_until_slide_will_be_active(3)
        banner.next()

        # Assertions
        banner.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/carousel/image/slide_1.png"
        )
