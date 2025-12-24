from selene import Element, have
from selene.support.conditions.have import text

from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Text, Button, Link
from src.util.decorator.step_logger import step_log

_SUCCESS_ADD_PRODUCT_TO_CART_MESSAGE = "Your product has been added to cart."
_NOT_AUTHORIZED_MESSAGE = "Register / Login account to proceed on checkout."


class NotificationComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self.__locator = _NotificationComponentLocator(root)

    # ACTIONS
    def close(self) -> None:
        self.__locator.close().click()

    def navigate(self) -> None:
        self.__locator.link().navigate()

    # ASSERTIONS
    def check_notification_has_title(self, text: str) -> None:
        self.__locator.title().should_have_text(text)

    def check_notification_has_description(self, text: str) -> None:
        self.__locator.description().should_have_text(text)

    def check_notification_has_success_added_product_message(self) -> None:
        self.__locator.description().should_have_text(
            _SUCCESS_ADD_PRODUCT_TO_CART_MESSAGE
        )

    def check_notification_is_not_success_added_product(self) -> None:
        self.__locator.description().should_not_have(
            text(_SUCCESS_ADD_PRODUCT_TO_CART_MESSAGE)
        )

    def check_notification_has_not_authorized_message(self) -> None:
        self.__locator.description().should_have_text(_NOT_AUTHORIZED_MESSAGE)

    def check_notification_has_link(self, text: str) -> None:
        self.__locator.description().should(have.attribute("href", text))

    def check_notification_has_link_text(self, text: str) -> None:
        self.__locator.link_text().should_have_text(text)

    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self.__locator.title().should_be_visible()
        self.__locator.description().should_be_visible()
        self.__locator.link().should_be_visible()
        self.__locator.close().should_be_visible()

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self.__locator.title().should_not_exists()
        self.__locator.description().should_not_exists()
        self.__locator.link().should_not_exists()
        self.__locator.close().should_not_exists()


class _NotificationComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def title(self) -> Text:
        return Text(self.__root.element("h4"), "Notification title")

    def description(self) -> Text:
        return Text(
            self.__root.element(".modal-body p:first-child"), "Notification description"
        )

    def link(self) -> Link:
        return Link(self.__root.element(".modal-body a"), "Notification link")

    def link_text(self) -> Text:
        return Text(self.__root.element(".modal-body a"), "Notification link text")

    def close(self) -> Button:
        return Button(self.__root.element(".btn-success"), "Notification close button")
