import os
import time
from abc import abstractmethod, ABC

from PIL import Image
from selene import browser, query

from src.config.config import CFG
from src.ui.component.common.header_component import HeaderComponent
from src.ui.component.common.notification_component import NotificationComponent
from src.ui.component.common.page_scroller_component import PageScrollerComponent
from src.ui.component.common.subscription_component import SubscriptionComponent
from src.util import system_util
from src.util.allure.step_logger import step_log
from src.util.screenshot import screenshot_util
from src.util.screenshot.image_util import create_blank_image
from src.util.screenshot.screen_diff import ScreenDiffResult
from src.util.string_util import StringUtil


class BasePage(ABC):

    def __init__(self):
        self._page_name = self.__get_page_name()
        self._header_component = HeaderComponent(browser.element("header"))
        self._page_scroller_component = PageScrollerComponent(
            browser.element("#scrollUp")
        )
        self._notification_component = NotificationComponent(
            browser.element(".modal-content")
        )
        self._subscription_component = SubscriptionComponent(
            browser.element("#footer .single-widget")
        )
        self._page_container = browser.element("body")

    # COMPONENTS
    @property
    def header(self) -> HeaderComponent:
        return self._header_component

    @property
    def page_scroller(self) -> PageScrollerComponent:
        return self._page_scroller_component

    @property
    def notification(self) -> NotificationComponent:
        return self._notification_component

    @property
    def subscription(self) -> SubscriptionComponent:
        return self._subscription_component

    # ACTIONS
    @step_log.log("Refresh browser page")
    def reload_page(self):
        browser.driver.refresh()

    def check_page_has_screenshot(
            self,
            path_to_screenshot: str,
            percent_of_tolerance: float = 0,
            rewrite_screenshot: bool = False,
            timeout: float = 0,
    ) -> None:
        """
        Checks if the page screenshot matches the expected screenshot.
        """
        self.check_page_is_visible()
        if timeout > 0:
            time.sleep(timeout)

        actual_screenshot = browser.get(query.screenshot_saved())
        screenshot_util.compare_and_save_screenshot(
            actual_screenshot = actual_screenshot,
            path_to_screenshot=path_to_screenshot,
            percent_of_tolerance=percent_of_tolerance,
            rewrite_screenshot=rewrite_screenshot,
            component_name=self._page_name
        )

    @abstractmethod
    def check_page_is_visible(self):
        pass

    @abstractmethod
    def check_page_is_not_visible(self):
        pass

    def __get_page_name(self) -> str:
        return StringUtil.camel_case_to_normal(type(self).__name__)
