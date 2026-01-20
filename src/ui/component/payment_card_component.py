from typing import Union

import allure
from selene import have, be
from selene.core.entity import Element

from src.model.card import CardInfo
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Input, Text, Button
from src.util.decorator.step_logger import step_log

_SUCCESS_PAYMENT_MESSAGE = "Your order has been placed successfully!"


class PaymentCardComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str):
        super().__init__(root, component_title)
        self.__locator = _PaymentCardComponentLocator(self._root)

    # ACTIONS
    @step_log.log("Pay by card")
    def pay(self, card_info: CardInfo):
        self.__fill_form(card_info)
        self.__submit()

    def pay_and_check_payment_success(self, card_info: CardInfo):
        self.pay_and_check_status_message(card_info, _SUCCESS_PAYMENT_MESSAGE)

    def pay_and_check_status_message(self, card_info: CardInfo, message: str):
        with step_log.log("Pay by card"):
            self.__fill_form(card_info)
            allure.step(f"Click on {self.__locator.pay().element_title} button")
        with step_log.log(f"Check payment status has message: {message}"):
            self.__submit_and_check_status_message(message)

    @step_log.log("Fill card data")
    def __fill_form(self, card_info: CardInfo):
        self.__fill_card_name(card_info.name)
        self.__fill_card_number(card_info.number)
        self.__fill_cvc(card_info.cvc)
        self.__fill_expiration_month(card_info.expiry_month)
        self.__fill_expiration_year(card_info.expiry_year)

    def __fill_card_name(self, card_name: str):
        self.__locator.card_name().set_value(card_name)

    def __fill_card_number(self, card_number: str):
        self.__locator.card_number().set_value(card_number)

    def __fill_cvc(self, cvc: str):
        self.__locator.cvc().set_value(cvc)

    def __fill_expiration_month(self, month: Union[str, int]):
        self.__locator.expiration_month().set_value(month)

    def __fill_expiration_year(self, year: Union[str, int]):
        self.__locator.expiration_year().set_value(year)

    def __submit(self):
        self.__locator.pay().click()

    def __submit_and_check_status_message(self, message: str):
        from selene import browser

        result = browser.driver.execute_async_script(
            """
            const callback = arguments[arguments.length - 1];
            const expectedText = arguments[0];

            const button = document.querySelector('[data-qa=pay-button]');
            const alertSelector = '.alert';

            if (!button) {
                callback({
                    success: false,
                    error: 'Pay button not found'
                });
                return;
            }

            button.click();

            const startTime = Date.now();
            const timeout = 2000;

            (function waitForAlert() {
                const alert = document.querySelector(alertSelector);

                if (alert && alert.offsetParent !== null) {
                    const actualText = alert.textContent.trim();

                    callback({
                        success: actualText.includes(expectedText),
                        actualText: actualText
                    });
                    return;
                }

                if (Date.now() - startTime > timeout) {
                    callback({
                        success: false,
                        error: 'Status message did not appear'
                    });
                    return;
                }

                requestAnimationFrame(waitForAlert);
            })();
            """,
            message,
        )

        if not result.get("success"):
            raise AssertionError(
                f"Status message check failed. Expected text: '{message}'. Actual result: {result}"
            )

    # ASSERTIONS
    @step_log.log("Check payment is successful")
    def check_payment_status_is_successful(self) -> None:
        """!!! Status message hides after 5 seconds"""
        self.__locator.status_message().should(be.visible)
        self.__locator.status_message().should(have.text(_SUCCESS_PAYMENT_MESSAGE))

    @step_log.log("Check payment status has expected message: {message}")
    def check_payment_status_has_expected_message(self, message: str) -> None:
        """!!! Status message hides after 5 seconds"""
        self.__locator.status_message().should(be.visible)
        self.__locator.status_message().should(have.text(message))

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
        return Input(self.__root.element("[data-qa=name-on-card]"), "Name on card")

    def card_number(self) -> Input:
        return Input(self.__root.element("[data-qa=card-number]"), "Card number")

    def cvc(self) -> Input:
        return Input(self.__root.element("[data-qa=cvc]"), "CVC")

    def expiration_month(self) -> Input:
        return Input(self.__root.element("[data-qa=expiry-month]"), "Expiration month")

    def expiration_year(self) -> Input:
        return Input(self.__root.element("[data-qa=expiry-year]"), "Expiration year")

    def status_message(self) -> Text:
        return Text(self.__root.element(".alert"), "Status message")

    def pay(self) -> Button:
        return Button(
            self.__root.element("[data-qa=pay-button]"), "Pay And Confirm Order"
        )
