from selene import browser, Element

from src.ui.component.address_component import AddressDetailsComponent
from src.ui.component.product.product_item_component import ProductItemComponent
from src.ui.component.product.products_items_collection_component import (
    ProductItemsComponent,
)
from src.ui.element.base_element import Button, UiElement, Input
from src.ui.page.base_page import BasePage
from src.util.decorator.step_logger import step_log

URL = "/checkout"


class CheckoutPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__locator = _CheckoutPageLocator(self._page_container)
        self.__delivery_address = AddressDetailsComponent.from_element(
            self.__locator.delivery_address()
        )
        self.__billing_address = AddressDetailsComponent.from_element(
            self.__locator.billing_address()
        )
        self.__product_items_component = ProductItemsComponent[ProductItemComponent](
            root=self.__locator.products_container().locator,
            component_title=self.__locator.products_container().element_title,
            cls=ProductItemComponent,
        )

    # COMPONENTS
    @property
    def delivery_address_component(self) -> AddressDetailsComponent:
        return self.__delivery_address

    @property
    def billing_address_component(self) -> AddressDetailsComponent:
        return self.__billing_address

    @property
    def products(self) -> ProductItemsComponent[ProductItemComponent]:
        return self.__product_items_component

    # ACTIONS
    @step_log.log("Open [Checkout Page]: {URL}")
    def navigate(self) -> None:
        browser.open(URL)

    @step_log.log("Add order message: {message}")
    def add_comment(self, message) -> None:
        self.__locator.message().set_value(message)

    @step_log.log("Submit order")
    def place_order(self) -> None:
        self.__locator.place_order().click()

    # ASSERTIONS
    @step_log.log("Check [{self._page_name}] is visible}]")
    def check_page_is_visible(self):
        self.__product_items_component.check_component_is_visible()

    @step_log.log("Check [{self._page_name}] is not visible}]")
    def check_page_is_not_visible(self):
        self.__product_items_component.check_component_is_not_exists()


class _CheckoutPageLocator:

    def __init__(self, root: Element):
        self.__root = root

    def delivery_address(self):
        return UiElement(self.__root.element("#address_delivery"), "Delivery Address")

    def billing_address(self):
        return UiElement(self.__root.element("#address_invoice"), "Billing Address")

    def message(self) -> Input:
        return Input(self.__root.element("[name=message]"), "Order Message")

    def place_order(self) -> Button:
        return Button(self.__root.element("//*[text()='Place Order']"), "Place Order")

    def products_container(self) -> UiElement:
        return UiElement(self.__root.element("#cart_info table"), "Cart products")
