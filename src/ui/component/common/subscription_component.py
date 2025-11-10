import allure
from selene import Element, have, be
from selene.support.conditions import not_

from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Input, Button, UiElement, Text
from src.util.step_logger import step_log

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
        with allure.step("Press submit subscription button"):
            self.__locator.submit()

    # ASSERTIONS
    def check_subscribe_status_message_is_visible(self) -> None:
        with allure.step("Close notification"):
            self.__locator.status_message_wrapper().should(be.visible)

    def check_success_subscribe_status_message_has_text(self, text: str) -> None:
        with allure.step(f"Check success subscribe status message has text: {_SUCCESS_SUBSCRIPTION_MESSAGE}"):
            self.__locator.status_message().should(have.text(text))

    def check_subscribe_component_has_screenshot(
        self, path_to_screenshot: str, percent_of_tolerance: float, rewrite_screenshot: bool
    ) -> None:
        with allure.step("Check subscribe component has screenshot"):
            self._check_element_have_screenshot(
                element=self._root,
                path_to_screenshot=path_to_screenshot,
                percent_of_tolerance=percent_of_tolerance,
                rewrite_screenshot=rewrite_screenshot,
            )

    def check_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are visible"):
            self.__locator.email().should(be.visible)
            self.__locator.submit().should(be.visible)

    def check_not_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are not exists"):
            self.__locator.email().should(not_.existing)
            self.__locator.submit().should(not_.existing)


class _SubscriptionComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def email(self) -> Input:
        return Input(self.__root.element("[type=email]"), "Email")

    def submit(self) -> Button:
        return Button(self.__root.element("button"), "Submit")

    def status_message_wrapper(self) -> UiElement:
        return UiElement(self.__root.element(".//ancestor::footer").element("#success-subscribe"), "Status message wrapper")

    def status_message(self) -> Text:
        return self.status_message_wrapper().element(".close-modal", "Status message", Text)

    def description(self) -> Text:
        return Text(self.__root.element("p"), "Description")
