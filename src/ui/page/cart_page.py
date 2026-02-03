from selene import browser, Element

from src.ui.component.product.product_item_component import (
    RemovableProductItemComponent,
)
from src.ui.component.product.products_items_collection_component import (
    ProductItemsComponent,
)
from src.ui.element.base_element import Button, UiElement
from src.ui.page.base_page import BasePage
from src.util.decorator.step_logger import step_log

URL = "/view_cart"


class CartPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__locator = _CartPageLocator(self._page_container)
        self.__product_cards_component = ProductItemsComponent[
            RemovableProductItemComponent
        ](
            root=self.__locator.products_container().locator,
            component_title=self.__locator.products_container().element_title,
            cls=RemovableProductItemComponent,
        )

    # COMPONENTS
    @property
    def products(self) -> ProductItemsComponent[RemovableProductItemComponent]:
        return self.__product_cards_component

    # ACTIONS
    @step_log.log("Open [Cart Page]: {URL}")
    def navigate(self) -> None:
        browser.open(URL)

    @step_log.log("Proceed to Checkout")
    def proceed_to_checkout(self) -> None:
        self.__locator.proceed_to_checkout().click()

    @step_log.log("Check cart is empty")
    def check_cart_is_empty(self):
        self.__locator.empty_cart().should_be_visible()

    @step_log.log("Check [{self._page_name}] is visible}]")
    def check_page_is_visible(self):
        self.__product_cards_component.check_component_is_visible()

    @step_log.log("Check [{self._page_name}] is not visible}]")
    def check_page_is_not_visible(self):
        self.__product_cards_component.check_component_is_not_exists()


class _CartPageLocator:

    def __init__(self, root: Element):
        self.__root = root

    def proceed_to_checkout(self) -> Button:
        return Button(
            self.__root.element("//*[text()='Proceed To Checkout']"),
            "Proceed to Checkout",
        )

    def empty_cart(self) -> UiElement:
        return UiElement(self.__root.element("#empty_cart"), "Empty Cart")

    def products_container(self) -> UiElement:
        return UiElement(self.__root.element("#cart_info table"), "Cart products")
