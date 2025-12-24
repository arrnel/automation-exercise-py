from abc import ABC

from selene import Element, browser
from typing_extensions import override

from src.ui.element.base_element import Text, ElementsCollection, Button
from src.ui.page.base_page import BasePage
from src.util.decorator.step_logger import step_log


class BaseConfirmationPage(BasePage, ABC):
    """Base Page for typical confirmation-pages (account created, deleted, order placed)"""

    _PAGE_TITLE: str = ""
    _PAGE_MESSAGES: tuple[str, ...] = ()

    def __init__(self, page_name: str):
        super().__init__()
        self._page_name = page_name
        self._root = browser.element("section .container")
        self._locator = _BaseConfirmationPageLocators(self._root, self._page_name)

    # ACTIONS
    def submit(self) -> None:
        self._locator.submit().click()

    # ASSERTIONS
    @step_log.log("Check [{self._page_name}] title and message have expected texts")
    def check_title_and_message_have_expected_texts(self) -> None:
        self._locator.title().should_have_text(self._PAGE_TITLE)
        self._locator.messages().should_contains_texts(*self._PAGE_MESSAGES)

    @step_log.log("Check [{self._page_name}] is visible")
    def check_page_is_visible(self) -> None:
        self._locator.title().should_be_visible()
        self._locator.submit().should_be_visible()

    @step_log.log("Check [{self._page_name}] is not visible")
    def check_page_is_not_visible(self) -> None:
        self._locator.title().should_not_exists()
        self._locator.submit().should_not_exists()


class AccountCreatedPage(BaseConfirmationPage):
    _PAGE_TITLE = "ACCOUNT CREATED!"
    _PAGE_MESSAGES = (
        "Congratulations! Your new account has been successfully created!",
        (
            "You can now take advantage of member privileges to enhance your "
            "online shopping experience with us."
        ),
    )

    def __init__(self):
        super().__init__("Account Created")


class AccountDeletedPage(BaseConfirmationPage):
    _PAGE_TITLE = "ACCOUNT DELETED!"
    _PAGE_MESSAGES = (
        "Your account has been permanently deleted!",
        (
            "You can create new account to take advantage of member privileges "
            "to enhance your online shopping experience with us."
        ),
    )

    def __init__(self):
        super().__init__("Account Deleted")


class OrderPlacedPage(BaseConfirmationPage):
    _PAGE_TITLE = "ORDER PLACED!"
    _PAGE_MESSAGES = ("Congratulations! Your order has been confirmed!",)

    def __init__(self):
        super().__init__("Order Placed")

    def download_invoice(self) -> None:
        self._locator.download_invoice().click()

    @override
    @step_log.log("Check [{self._page_name}] is visible")
    def check_page_is_visible(self) -> None:
        self._locator.title().should_be_visible()
        self._locator.submit().should_be_visible()
        self._locator.download_invoice().should_be_visible()

    @override
    @step_log.log("Check [{self._page_name}] is not visible")
    def check_page_is_not_visible(self) -> None:
        self._locator.title().should_not_exists()
        self._locator.submit().should_not_exists()
        self._locator.download_invoice().should_not_exists()


class _BaseConfirmationPageLocators:

    def __init__(self, root: Element, page_name: str):
        self._root = root
        self._page_name = page_name

    def title(self) -> Text:
        return Text(self._root.element("h2 b"), f"{self._page_name} title")

    def messages(self) -> ElementsCollection:
        return ElementsCollection(
            self._root.all("p"), f"{self._page_name} messages", Text
        )

    def submit(self) -> Button:
        return Button(self._root.element("[data-qa=continue-button]"), "Continue")

    def download_invoice(self) -> Button:
        return Button(
            self._root.element("a[href^='/download_invoice']"), "Download Invoice"
        )
