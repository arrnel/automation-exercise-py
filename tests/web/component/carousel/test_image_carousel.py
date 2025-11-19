from src.ui.page.auth.login_page import LoginPage
from src.ui.page.main_page import MainPage


class TestImageCarousel:

    def setup_method(self):
        self.login_page = LoginPage()
        self.main_page = MainPage()

    def test_should_show_previous_image_when_scroll_left(self, browser_open):
        pass

    def test_should_show_next_image_when_scroll_right(self, browser_open):
        pass

    def test_should_show_last_image_when_scroll_left_on_first_image(self, browser_open):
        pass

    def test_should_show_first_image_when_scroll_right_on_last_image(
        self, browser_open
    ):
        pass
