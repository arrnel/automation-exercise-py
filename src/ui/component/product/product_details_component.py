from typing import Optional

from selene import Element

from src.model.category import Category
from src.model.price import Price
from src.model.product import Product
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import (
    Button,
    Text,
    UiElement,
    Input,
    ElementsCollection,
)
from src.util.decorator.step_logger import step_log


class ProductDetailsComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)
        self._locator = _ProductDetailsComponentLocator(self._root)

    # ACTIONS
    def get_product_id(self) -> int:
        return int(self._locator.product_id().get_value())

    @step_log.log("Add {count} [{self._component_title}] product(s) to cart")
    def add_products_to_cart(self, count: int) -> None:
        self._locator.quantity().set_value(count)
        self._locator.add_to_cart().click()

    @step_log.log("Add [{self._component_title}] product to cart")
    def add_to_cart(self) -> None:
        self._locator.add_to_cart().click()

    # ASSERTIONS
    @step_log.log("Check product [{self._component_title}] has expected data")
    def check_product_has_data(self, product_info: Product):
        self.check_product_has_title(product_info.title)
        self.check_product_has_category(product_info.category)
        self.check_product_has_price(product_info.price)
        self.check_product_has_availability(product_info.availability)
        self.check_product_has_condition(product_info.condition)
        self.check_product_has_brand(product_info.brand)

    def check_product_has_id(self, product_id: int) -> None:
        self._locator.product_id().should_have_value(product_id)

    @step_log.log("Check product [{self._component_title}] has title: {title}")
    def check_product_has_title(self, title: str) -> None:
        self._locator.title().should_have_text(title)

    def check_product_has_category(self, category: Category) -> None:
        group = category.user_type.value
        category = category.title
        with step_log.log(
            f"Check product [{self._component_title}] "
            f"has group = [{group}] and category = [{category}]"
        ):
            self._locator.category().should_have_text(f"Category: {group} > {category}")

    def check_product_has_price(self, price: Price) -> None:
        with step_log.log(
            f"Check product [{self._component_title}] has price: {price.get_amount_text()}"
        ):
            self._locator.price().should_have_text(price.get_price_text())

    @step_log.log("Check product [{self._component_title}] has availability: {status}")
    def check_product_has_availability(self, status: str):
        self._locator.availability().should_have_text(f"Availability: {status}")

    @step_log.log("Check product [{self._component_title}] has condition: {condition}")
    def check_product_has_condition(self, condition: str):
        self._locator.condition().should_have_text(f"Condition: {condition}")

    @step_log.log("Check product [{self._component_title}] has condition: {brand}")
    def check_product_has_brand(self, brand: str):
        self._locator.brand().should_have_text(f"Brand: {brand}")

    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self._locator.img().should_be_visible()
        self._locator.price().should_be_visible()
        self._locator.title().should_be_visible()
        self._locator.add_to_cart().should_be_visible()

    @step_log.log("Check [{self._component_title}] elements are not existing")
    def check_not_visible_component_elements(self) -> None:
        self._locator.img().should_not_exists()
        self._locator.price().should_not_exists()
        self._locator.title().should_not_exists()
        self._locator.add_to_cart().should_not_exists()


class _ProductDetailsComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def product_id(self) -> Input:
        return Input(self.__root.element("#product_id"), "Product id")

    def img(self) -> UiElement:
        return UiElement(self.__root.element(".view-product img"), "Product image")

    def new_arrival(self) -> Text:
        return Text(
            self.__root.element(".product-information img"), "Product New Arrival Badge"
        )

    def title(self) -> Text:
        return Text(self.__root.element(".product-information h2"), "Product Rating")

    def category(self) -> Text:
        return Text(self.__root.element(".product-information p"), "Product Category")

    def rating(self) -> UiElement:
        return UiElement(
            self.__root.element(".product-information p"), "Product Rating"
        )

    def price(self) -> Text:
        return Text(
            self.__root.element(".product-information span span"), "Product Price"
        )

    def quantity(self) -> Input:
        return Input(self.__root.element("#quantity"), "Product Quantity")

    def add_to_cart(self) -> Button:
        return Button(self.__root.element("button.cart"), "Add to cart")

    def characteristics(self) -> ElementsCollection:
        return ElementsCollection(
            self.__root.all(".//p[./b]"), "Product Characteristics"
        )

    def availability(self) -> Text:
        return Text(self.__root.element("//p[./b][1]"), "Product Availability")

    def condition(self) -> Text:
        return Text(self.__root.element("//p[./b][2]"), "Product Condition")

    def brand(self) -> Text:
        return Text(self.__root.element("//p[./b][3]"), "Product Brand")
