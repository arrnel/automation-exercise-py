from enum import Enum

import allure
from selene import Element, be

from src.model.address import AddressInfo
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Text
from src.util.decorator.step_logger import step_log

_COMPANY_ADDRESS_LINE_SELECTOR = "//li[contains(@class,'address-address1')][%d]"
_DELIVERY_ADDRESS_TITLE = "Your delivery address"
_BILLING_ADDRESS_TITLE = "Your billing address"


class AddressType(Enum):
    DELIVERY = ("Delivery address",)
    BILLING_ADDRESS = "Billing address"


class AddressDetailsComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str) -> None:
        super().__init__(root, component_title)
        self.__locator = _AddressDetailsComponentLocator(root)

    # ASSERTIONS
    @step_log.log("Check [{self._component_title}] has address info")
    def check_have_address_info(self, address_info) -> None:
        with allure.step(f"Check [{self._component_title}] has address info"):
            self._root.should(be.visible)
            actual_address_info = AddressInfo(
                title=self.__locator.title().get_text(),
                full_name=self.__locator.full_name().get_text(),
                company=self.__locator.company().get_text(),
                address1=self.__locator.address1().get_text(),
                address2=self.__locator.address2().get_text(),
                city_state_zip=self.__locator.city_state_zip().get_text(),
                country=self.__locator.country().get_text(),
                phone_number=self.__locator.phone_number().get_text(),
            )

            if not address_info.equals(actual_address_info):
                raise AssertionError(
                    (
                        "Expected and actual addresses not equals:\n",
                        f"Expected: {address_info}\n",
                        f"Actual: {actual_address_info}\n",
                    )
                )

    def check_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are visible"):
            self.__locator.title().should_be_visible()
            self.__locator.full_name().should_be_visible()

    def check_not_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are not exists"):
            self.__locator.title().should_not_exists()
            self.__locator.full_name().should_not_exists()


class _AddressDetailsComponentLocator:

    def __init__(self, root: Element):
        self.root = root

    def title(self) -> Text:
        return Text(self.root.element("h3"), "Address Title")

    def full_name(self) -> Text:
        return Text(self.root.element(".address_firstname"), "Full Name")

    def company(self) -> Text:
        return Text(self.root.element(_COMPANY_ADDRESS_LINE_SELECTOR % 1), "Company")

    def address1(self) -> Text:
        return Text(self.root.element(_COMPANY_ADDRESS_LINE_SELECTOR % 2), "Address 1")

    def address2(self) -> Text:
        return Text(self.root.element(_COMPANY_ADDRESS_LINE_SELECTOR % 3), "Address 2")

    def city_state_zip(self) -> Text:
        return Text(self.root.element(".address_city"), "City, State, Zip Code")

    def country(self) -> Text:
        return Text(self.root.element(".address_country_name"), "Country")

    def phone_number(self) -> Text:
        return Text(self.root.element(".address_phone"), "Mobile Phone")

    def close(self) -> Text:
        return Text(self.root.element(".close-modal"), "")
