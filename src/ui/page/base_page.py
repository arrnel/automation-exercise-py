from abc import abstractmethod, ABC

from selene import browser, query

from src.ui.component.common.header_component import HeaderComponent
from src.ui.component.common.notification_component import NotificationComponent
from src.ui.component.common.page_scroller_component import PageScrollerComponent
from src.ui.component.common.subscription_component import SubscriptionComponent
from src.util.step_logger import step_log
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

    # ACTIONS
    @step_log.log("Refresh browser page")
    def reload_page(self):
        browser.driver.refresh()

    # ASSERTIONS
    # def check_header_has_screenshot(
    #     self, path_to_screenshot: str, percent_of_tolerance: float = 0, rewrite_screenshot=False, timeout: int = 0
    # ):
    #     with allure.step("Check [Header] has screenshot"):
    #         self._header_component.check_component_has_screenshot(path_to_screenshot, percent_of_tolerance, rewrite_screenshot, timeout)
    #
    # def check_page_scroller_has_screenshot(
    #     self, path_to_screenshot: str, percent_of_tolerance: float = 0, rewrite_screenshot=False, timeout: int = 0
    # ):
    #     with allure.step("Check [Page Scroller] has screenshot"):
    #         self._page_scroller_component.check_component_has_screenshot(
    #             path_to_screenshot, percent_of_tolerance, rewrite_screenshot, timeout
    #         )
    #
    # def check_notification_has_screenshot(
    #     self, path_to_screenshot: str, percent_of_tolerance: float = 0, rewrite_screenshot=False, timeout: int = 0
    # ):
    #     with allure.step("Check [Notification] form has screenshot"):
    #         self._notification_component.check_component_has_screenshot(
    #             path_to_screenshot, percent_of_tolerance, rewrite_screenshot, timeout
    #         )
    #
    # def check_subscription_component_has_screenshot(
    #     self, path_to_screenshot: str, percent_of_tolerance: float = 0, rewrite_screenshot=False, timeout: int = 0
    # ):
    #     with allure.step("Check [Subscription] form has screenshot"):
    #         self._subscription_component.check_component_has_screenshot(
    #             path_to_screenshot, percent_of_tolerance, rewrite_screenshot, timeout
    #         )

    def check_page_has_screenshot(self):
        browser.get(query.screenshot_saved())

    @abstractmethod
    def check_page_is_visible(self):
        pass

    @abstractmethod
    def check_page_is_not_visible(self):
        pass

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

    def __get_page_name(self) -> str:
        return StringUtil.camel_case_to_normal(type(self).__name__)
