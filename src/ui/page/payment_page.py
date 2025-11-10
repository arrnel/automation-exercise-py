from src.ui.component.payment_card_component import PaymentCardComponent
from src.ui.page.base_page import BasePage


class PaymentPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__payment_card_component = PaymentCardComponent(
            self._page_container.element("#payment-form"), "Payment Form"
        )

    # COMPONENTS
    @property
    def payment_card_component(self) -> PaymentCardComponent:
        return self.__payment_card_component

    # ASSERTIONS
    def check_page_is_visible(self) -> None:
        self.__payment_card_component.check_component_is_visible()

    def check_page_is_not_visible(self):
        self.__payment_card_component.check_component_is_not_exists()
