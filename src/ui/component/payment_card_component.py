from typing import Union

from selene import have, be
from selene.core.entity import Element

from src.model.card import CardInfo
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Input, Text, Button
from src.util.step_logger import step_log

_SUCCESS_PAYMENT_MESSAGE = "Your order has been placed successfully!"


class PaymentCardComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str):
        super().__init__(root, component_title)
        self.__locator = _PaymentCardComponentLocator(self._root)

    # ACTIONS
    @step_log.log("Pay by card")
    def pay(self, card_info: CardInfo):
        self.__fill_card_name(card_info.name)
        self.__fill_card_number(card_info.name)
        self.__fill_cvc(card_info.name)
        self.__fill_expiration_month(card_info.name)
        self.__fill_expiration_year(card_info.name)
        self.__submit()

    def __fill_card_name(self, card_name: str):
        self.__locator.card_name().set_value(card_name)

    def __fill_card_number(self, card_number: str):
        self.__locator.card_number().set_value(card_number)

    def __fill_cvc(self, cvc: str):
        self.__locator.cvc().set_value(cvc)

    def __fill_expiration_month(self, month: Union[str, int]):
        self.__locator.cvc().set_value(month)

    def __fill_expiration_year(self, year: Union[str, int]):
        self.__locator.cvc().set_value(year)

    def __submit(self):
        self.__locator.pay().click()

    # ASSERTIONS
    @step_log.log("Check payment is successful")
    def check_payment_successful(self) -> None:
        """!!! Status message hides after 5 seconds"""
        self.__locator.status_message().should(be.visible)
        self.__locator.status_message().should(have.text(_SUCCESS_PAYMENT_MESSAGE))

    def check_visible_component_elements(self) -> None:
        self.__locator.card_name().should_be_visible()
        self.__locator.card_number().should_be_visible()
        self.__locator.cvc().should_be_visible()
        self.__locator.expiration_month().should_be_visible()
        self.__locator.expiration_year().should_be_visible()
        self.__locator.pay().should_be_visible()

    def check_not_visible_component_elements(self) -> None:
        self.__locator.card_name().should_not_exists()
        self.__locator.card_number().should_not_exists()
        self.__locator.cvc().should_not_exists()
        self.__locator.expiration_month().should_not_exists()
        self.__locator.expiration_year().should_not_exists()
        self.__locator.pay().should_not_exists()


class _PaymentCardComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def card_name(self) -> Input:
        return Input(self.__root.element("[name=name_on_card]"), "Name on card")

    def card_number(self) -> Input:
        return Input(self.__root.element("[name=card_number]"), "Card number")

    def cvc(self) -> Input:
        return Input(self.__root.element("[name=cvc]"), "CVC")

    def expiration_month(self) -> Input:
        return Input(self.__root.element("[name=expiry_month]"), "Expiration month")

    def expiration_year(self) -> Input:
        return Input(self.__root.element("[name=expiry_year]"), "Expiration year")

    def status_message(self) -> Text:
        return Text(self.__root.element(".alert"), "Status message")

    def pay(self) -> Button:
        return Button(self.__root.element("[data-qa=pay-button]"), "Pay And Confirm Order")
