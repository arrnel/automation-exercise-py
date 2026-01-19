from selene import Element

from src.model.contact import ContactInfo
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Input, Button, Text
from src.util.decorator.step_logger import step_log

_SUCCESS_MESSAGE = "Success! Your details have been submitted successfully."


class ContactUsComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str):
        super().__init__(root, component_title)
        self.__locator = _ContactUsComponentLocator(self._root)

    # ACTIONS
    @step_log.log('Send "Contact Us" form')
    def send(self, contact_info: ContactInfo) -> None:
        self.__fill_form(contact_info)
        self.__submit()

    @step_log.log('Fill "Contact Us" form')
    def __fill_form(self, contact_info: ContactInfo) -> None:
        self.__fill_name(contact_info.name)
        self.__fill_email(contact_info.email)
        self.__fill_subject(contact_info.subject)
        self.__fill_message(contact_info.message)
        self.__upload_file(contact_info.path_to_file)

    def __fill_name(self, name: str) -> None:
        self.__locator.name().set_value(name)

    def __fill_email(self, email: str) -> None:
        self.__locator.email().set_value(email)

    def __fill_subject(self, subject: str) -> None:
        self.__locator.subject().set_value(subject)

    def __fill_message(self, message: str) -> None:
        self.__locator.message().set_value(message)

    def __upload_file(self, path_to_file: str) -> None:
        self.__locator.upload_file().set_value(path_to_file)

    def __submit(self) -> None:
        self.__locator.submit().click()

    def home(self):
        self.__locator.home().click()

    # ASSERTIONS
    def check_status_message_has_expected_text(self) -> None:
        self.__locator.status_message().should_have_text(_SUCCESS_MESSAGE)

    def check_visible_component_elements(self) -> None:
        """Check is valid if contact form is not send"""
        self.__locator.name().should_be_visible()
        self.__locator.email().should_be_visible()
        self.__locator.subject().should_be_visible()
        self.__locator.message().should_be_visible()
        self.__locator.upload_file().should_be_visible()

    def check_not_visible_component_elements(self) -> None:
        self.__locator.name().should_not_exists()
        self.__locator.email().should_not_exists()
        self.__locator.subject().should_not_exists()
        self.__locator.message().should_not_exists()
        self.__locator.upload_file().should_not_exists()
        self.__locator.status_message().should_not_exists()
        self.__locator.home().should_not_exists()


class _ContactUsComponentLocator:

    def __init__(self, root: Element):
        self._root = root

    def name(self) -> Input:
        return Input(self._root.element("[name=name]"), "Name")

    def email(self) -> Input:
        return Input(self._root.element("[name=email]"), "Email")

    def subject(self) -> Input:
        return Input(self._root.element("[name=subject]"), "Subject")

    def message(self) -> Input:
        return Input(self._root.element("[name=message]"), "Message")

    def upload_file(self) -> Input:
        return Input(self._root.element("[name=upload_file]"), "Upload file")

    def submit(self) -> Button:
        return Button(self._root.element("[name=submit]"), "Submit")

    def status_message(self) -> Text:
        return Text(self._root.element(".status.alert"), "Status message")

    def home(self) -> Button:
        return Button(self._root.element(".btn-success"), "Status message")
