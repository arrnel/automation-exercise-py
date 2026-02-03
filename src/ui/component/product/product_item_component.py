from abc import ABC

from selene import Element, query
from selene.support.conditions.be import existing

from src.model.category import Category
from src.model.enum.user_type import UserType
from src.model.price import Price
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import UiElement, Text, Input, Button, TextLink
from src.util.decorator.step_logger import step_log


class BaseProductItemComponent(BaseComponent, ABC):
    """Base class of products list items (table rows in CartPage and CheckoutPage)"""

    def __init__(self, root: Element, component_title: str):
        super().__init__(root, component_title)
        self._locator = _ProductItemComponentLocator(self._root)

    def get_id(self) -> int:
        text = self._locator.id().get(query.attribute("id"))
        product_id = int(text.replace("product-", ""))
        return product_id

    def get_title(self) -> str:
        return self._locator.title().get_text()

    def get_category(self) -> Category:
        values = self._locator.category().get_text().split(" > ")
        return Category(user_type=UserType(values[0]), title=values[1])

    def get_price(self) -> Price:
        return Price.from_text(self._locator.price().get_text())

    def get_quantity(self) -> int:
        return int(self._locator.quantity().get_text())

    def get_total_price(self) -> Price:
        return Price.from_text(self._locator.total_price().get_text())

    def navigate_to_product(self) -> None:
        self._locator.title().click()

    @step_log.log("Check [{self._component_title}] has price: {price}")
    def check_item_have_price(self, price: Price) -> None:
        self._locator.price().should_have_text(price.get_amount_text())

    @step_log.log("Check [{self._component_title}] has quantity: {quantity}")
    def check_item_have_quantity(self, quantity: int) -> None:
        self._locator.quantity().should_have_value(quantity)

    @step_log.log("Check [{self._component_title}] has total price: {total_price}")
    def check_item_have_total_price(self, total_price: Price) -> None:
        self._locator.total_price().should_have_text(total_price.get_amount_text())

    @step_log.log("Check [{self._component_title}] has correct data")
    def should_have_data(self, price: Price, quantity: int, total_price: Price) -> None:
        self.check_item_have_price(price)
        self.check_item_have_quantity(quantity)
        self.check_item_have_total_price(total_price)


class ProductItemComponent(BaseProductItemComponent):
    """Component for products list items on CartPage, without removal button"""

    def __init__(self, root: Element, component_title: str):
        super().__init__(root, component_title)

    def check_visible_component_elements(self) -> None:
        self._locator.img().should_be_visible()
        self._locator.title().should_be_visible()
        self._locator.price().should_be_visible()
        self._locator.total_price().should_be_visible()
        self._locator.quantity().should_be_visible()

    def check_not_visible_component_elements(self) -> None:
        self._locator.img().should_not_exists()
        self._locator.title().should_not_exists()
        self._locator.price().should_not_exists()
        self._locator.total_price().should_not_exists()
        self._locator.quantity().should_not_exists()


class RemovableProductItemComponent(ProductItemComponent):
    """Component for products list items on CheckoutPage, with removal button"""

    def __init__(self, root: Element, component_title: str):
        super().__init__(root, component_title)

    @step_log.log("Remove [{self._component_title}]")
    def remove(self):
        self._locator.remove().click(by_js=True)
        self._locator.remove().wait_until_not(existing)

    def check_visible_component_elements(self) -> None:
        self._locator.img().should_be_visible()
        self._locator.title().should_be_visible()
        self._locator.price().should_be_visible()
        self._locator.total_price().should_be_visible()
        self._locator.quantity().should_be_visible()
        self._locator.remove().should_not_exists()

    def check_not_visible_component_elements(self) -> None:
        self._locator.img().should_not_exists()
        self._locator.title().should_not_exists()
        self._locator.price().should_not_exists()
        self._locator.total_price().should_not_exists()
        self._locator.quantity().should_not_exists()
        self._locator.remove().should_not_exists()


class _ProductItemComponentLocator:
    """Locators for ProductItemComponent"""

    def __init__(self, root: Element):
        self.__root = root

    def id(self):
        return self.__root

    def img(self) -> UiElement:
        return UiElement(self.__root.element(".cart_product img"), "Product Image")

    def title(self) -> TextLink:
        return TextLink(self.__root.element(".cart_description h4 a"), "Product Title")

    def category(self) -> Text:
        return Text(self.__root.element(".cart_description p"), "Product Category")

    def price(self) -> Text:
        return Text(self.__root.element(".cart_price p"), "Product Price")

    def quantity(self) -> Input:
        return Input(self.__root.element(".cart_quantity button"), "Product Quantity")

    def total_price(self) -> Text:
        return Text(self.__root.element(".cart_total p"), "Product Total Price")

    def remove(self) -> Button:
        return Button(self.__root.element(".cart_delete a"), "Product Remove")
