import io
import time
from abc import abstractmethod, ABC

from PIL import Image
from selene import browser

from src.config.config import CFG
from src.ui.component.common.header_component import HeaderComponent
from src.ui.component.common.notification_component import NotificationComponent
from src.ui.component.common.page_scroller_component import PageScrollerComponent
from src.ui.component.common.subscription_component import SubscriptionComponent
from src.util.decorator.step_logger import step_log
from src.util.screenshot import screenshot_util
from src.util.string_util import StringUtil


class BasePage(ABC):

    def __init__(self):
        self._page_name = self.__get_page_name()
        self._header_component = HeaderComponent(browser.element("header"), "Header")
        self._page_scroller_component = PageScrollerComponent(
            browser.element("#scrollUp"),
            "Page Scroller",
        )
        self._notification_component = NotificationComponent(
            browser.element(".modal-content"), "Notification Component"
        )
        self._subscription_component = SubscriptionComponent(
            browser.element("#footer .single-widget"),
            "Notification Component",
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
        percent_of_tolerance: float = CFG.default_percent_of_tolerance,
        rewrite_screenshot: bool = False,
        timeout: float = CFG.default_screenshot_timeout,
    ) -> None:
        """
        Checks if the page screenshot matches the expected screenshot.
        """
        self.check_page_is_visible()
        if timeout > 0:
            time.sleep(timeout)

        actual_screenshot_bytes = io.BytesIO(browser.driver.get_screenshot_as_png())
        actual_screenshot = Image.open(actual_screenshot_bytes)
        screenshot_util.compare_and_save_screenshot(
            actual_screenshot=actual_screenshot,
            path_to_screenshot=path_to_screenshot,
            percent_of_tolerance=percent_of_tolerance,
            rewrite_screenshot=rewrite_screenshot,
            component_name=self._page_name,
        )

    @abstractmethod
    def check_page_is_visible(self):
        pass

    @abstractmethod
    def check_page_is_not_visible(self):
        pass

    def __get_page_name(self) -> str:
        return StringUtil.camel_case_to_normal(type(self).__name__)
