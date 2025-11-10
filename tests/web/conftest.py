import pytest
from selene import browser, Browser

from src.config.config import CFG
from src.util.step_logger import step_log


@pytest.fixture()
def browser_open():

    browser.config.base_url = "https://automationexercise.com"
    browser.config.driver_name = CFG.browser_name
    browser.config.window_width = CFG.browser_size[0]
    browser.config.window_height = CFG.browser_size[1]
    browser.config.type_by_js = True
    browser.config.timeout = CFG.browser_timeout

    with step_log.log("Open browser: /login"):
        browser.open("/login")

    yield

    browser.quit()


class ChromeOptions:

    def process(self) -> Browser:
        from selenium.webdriver.chrome import webdriver

        options = webdriver.Options()
        options.add_argument("--headless")
