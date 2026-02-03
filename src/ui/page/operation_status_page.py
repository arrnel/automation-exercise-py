from abc import ABC

from selene import Element, browser
from typing_extensions import override

from src.config.config import CFG
from src.model.price import Price
from src.ui.element.base_element import (
    Text,
    ElementsCollection,
    Button,
    DownloadableButton,
)
from src.ui.page.base_page import BasePage
from src.util import system_util
from src.util.decorator.step_logger import step_log
from src.util.invoice_util import InvoiceUtil
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


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

    @step_log.log("Download invoice file with expected title: {expected_file_name}")
    def download_invoice(self, expected_file_name: str) -> str:
        """Returns path to downloaded file."""
        return self._locator.download_invoice().download(expected_file_name)

    def check_last_invoice_has_data(self, full_name: str, price: Price) -> None:
        path_to_invoice_dir = (
            f"{CFG.browser_download_dir}"
            f"/{ThreadSafeTestThreadsStore().current_thread_test_name()}"
        )
        invoice_file_name = system_util.get_files_in_directory(
            path_to_invoice_dir,
            file_extensions={"txt"},
            starts_with="invoice",
            order_by="date_time",
            order_direction="desc",
        )[0]
        path_to_invoice = f"{path_to_invoice_dir}/{invoice_file_name}"
        self.compare_invoice_data(path_to_invoice, full_name, price)

    def check_invoice_has_data(
        self,
        path_to_file: str,
        full_name: str,
        price: Price,
    ) -> None:
        self.compare_invoice_data(path_to_file, full_name, price)

    @step_log.log("Check invoice file has expected data")
    def compare_invoice_data(
        self, path_to_invoice: str, full_name: str, price: Price
    ) -> None:
        actual_full_name, actual_price = InvoiceUtil.parse_full_name_and_price(
            path_to_invoice
        )
        with step_log.log(f"Check invoice contains full name: {full_name}"):
            if full_name != actual_full_name:
                raise AssertionError(
                    f"Invoice full name does not match actual full name. "
                    f"Expected: {full_name}, "
                    f"Actual: {actual_full_name}"
                )
        with step_log.log(f"Check invoice contains price: {price}"):
            if price != actual_price:
                raise AssertionError(
                    f"Invoice price does not match actual price."
                    f"Expected: {price}, "
                    f"Actual: {actual_price}"
                )

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

    def download_invoice(self) -> DownloadableButton:
        return DownloadableButton(
            self._root.element("a[href^='/download_invoice']"), "Download Invoice"
        )
