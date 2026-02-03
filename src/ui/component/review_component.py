from typing import Optional

from selene import Element

from src.model.review import ReviewInfo
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Button, Text, Input
from src.util.decorator.step_logger import step_log

_SUCCESS_STATUS_MESSAGE = "Thank you for your review."


class ReviewComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)
        self._locator = _ProductDetailsComponentLocator(self._root)

    def send_review(self, review_info: ReviewInfo) -> None:
        self.__fill_name(review_info.name)
        self.__fill_email(review_info.email)
        self.__fill_message(review_info.message)
        self.__submit()

    def __fill_name(self, name: str) -> None:
        self._locator.name().set_value(name)

    def __fill_email(self, email: str) -> None:
        self._locator.email().set_value(email)

    def __fill_message(self, message: str) -> None:
        self._locator.message().set_value(message)

    def __submit(self) -> None:
        self._locator.submit().click()

    @step_log.log("Check review successfully send")
    def check_review_status_message_successful(self):
        self._locator.status_message().should_have_text(_SUCCESS_STATUS_MESSAGE)

    @step_log.log("Check review has error message: {text}")
    def check_review_status_message_has_text(self, text: str) -> None:
        self._locator.status_message().should_have_text(text)

    def check_visible_component_elements(self) -> None:
        self._locator.name().should_be_visible()
        self._locator.email().should_be_visible()
        self._locator.message().should_be_visible()
        self._locator.submit().should_be_visible()

    def check_not_visible_component_elements(self) -> None:
        self._locator.name().should_not_exists()
        self._locator.email().should_not_exists()
        self._locator.message().should_not_exists()
        self._locator.submit().should_not_exists()


class _ProductDetailsComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def name(self) -> Input:
        return Input(self.__root.element("#name"), "Name")

    def email(self) -> Input:
        return Input(self.__root.element("#email"), "Email")

    def message(self) -> Input:
        return Input(self.__root.element("#review"), "Message")

    def submit(self) -> Button:
        return Button(self.__root.element("#button-review"), "Submit")

    def status_message(self) -> Text:
        return Text(
            self.__root.element("#review-section span"), "Review Status Message"
        )
