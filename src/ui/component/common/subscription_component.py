from selene import Element, be
from selene.support.conditions import not_

from src.config.config import CFG
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Input, Button, UiElement, Text
from src.util.decorator.step_logger import step_log

_SUCCESS_SUBSCRIPTION_MESSAGE = "You have been successfully subscribed!"


class SubscriptionComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None) -> None:
        super().__init__(root, component_title)
        self.__locator = _SubscriptionComponentLocator(root)

    # ACTIONS
    @step_log.log("Subscribe by email: {email}")
    def subscribe(self, email: str) -> None:
        self.__fill_email(email)
        self.__submit()

    def __fill_email(self, email: str) -> None:
        self.__locator.email().set_value(email)

    def __submit(self) -> None:
        self.__locator.submit().click()

    # ASSERTIONS
    def check_subscribe_status_message_is_visible(self) -> None:
        self.__locator.status_message().should_be_visible()

    def check_success_subscribe_status_message_has_text(self, text: str) -> None:
        self.__locator.status_message().should_have_text(text)

    def check_subscribe_has_success_status_message(self) -> None:
        self.__locator.status_message().should_have_text(_SUCCESS_SUBSCRIPTION_MESSAGE)

    def check_component_with_status_message_has_screenshot(
        self,
        path_to_screenshot: str,
        percent_of_tolerance: float = CFG.default_percent_of_tolerance,
        rewrite_screenshot: bool = False,
        timeout: float = 0,
        hover: bool = False,
    ) -> None:
        self.__locator.subscription_and_status_wrapper().check_element_has_screenshot(
            path_to_screenshot=path_to_screenshot,
            percent_of_tolerance=percent_of_tolerance,
            rewrite_screenshot=rewrite_screenshot,
            hover=hover,
            timeout=timeout,
        )

    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self.__locator.email().should(be.visible)
        self.__locator.submit().should(be.visible)

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self.__locator.email().should(not_.existing)
        self.__locator.submit().should(not_.existing)


class _SubscriptionComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def subscription_and_status_wrapper(self):
        return UiElement(
            self.__root.element("./ancestor::div[@class='row']"),
            "Subscription component",
        )

    def submit(self) -> Button:
        return Button(self.__root.element("button"), "Submit")

    def email(self) -> Input:
        return Input(self.__root.element("[type=email]"), "Email")

    def status_message_wrapper(self) -> UiElement:
        return UiElement(
            self.__root.element(".//ancestor::footer").element("#success-subscribe"),
            "Status message wrapper",
        )

    def status_message(self) -> Text:
        return self.status_message_wrapper().element(".alert", "Status message", Text)

    def description(self) -> Text:
        return Text(self.__root.element("p"), "Description")
