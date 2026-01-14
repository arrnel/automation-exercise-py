from selene import browser

from src.ui.component.payment_card_component import PaymentCardComponent
from src.ui.page.base_page import BasePage
from src.util.decorator.step_logger import step_log

URL = "/payment"


class PaymentPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__payment_card_component = PaymentCardComponent(
            self._page_container.element(".payment-information"), "Payment Form"
        )

    # COMPONENTS
    @property
    def payment_card_component(self) -> PaymentCardComponent:
        return self.__payment_card_component

    @step_log.log("Open [Payment Page]: {URL}")
    def navigate(self):
        browser.open(URL)

    # ASSERTIONS
    def check_page_is_visible(self) -> None:
        self.__payment_card_component.check_component_is_visible()

    def check_page_is_not_visible(self):
        self.__payment_card_component.check_component_is_not_exists()
