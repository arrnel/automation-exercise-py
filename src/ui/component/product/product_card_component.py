from typing import Optional, override

from selene import Element

from src.model.price import Price
from src.model.product import Product
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Button, Text, UiElement
from src.util.decorator.step_logger import step_log

_DEFAULT_TIMEOUT_OVERLAY_WAIT = 0.2


class BaseProductCardComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)
        self._locator = _ProductCardComponentLocator(self._root)

    def get_product_title(self) -> str:
        return self._locator.title().get_text()

    def get_product_price(self) -> Price:
        return Price.from_text(self._locator.price().get_text())

    @step_log.log("Add product to cart: {self._component_title}")
    def add_to_cart(self) -> None:
        self._locator.add_to_cart().click()

    @step_log.log("Check product card [{self._component_title}] has title: {title}")
    def check_product_has_title(self, title: str) -> None:
        self._locator.title().should_have_text(title)

    @step_log.log("Check product card [{self._component_title}] has price: {price}")
    def check_product_has_price(self, price: Price) -> None:
        self._locator.price().should_have_text(price.get_price_text())

    @step_log.log("Check product card [{self._component_title}] has expected data")
    def check_product_card_has_data(self, product: Product) -> None:
        self.check_product_has_title(product.title)
        self.check_product_has_price(product.price)

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


class ProductCardComponent(BaseProductCardComponent):
    """Product card used in carousel"""

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)


class AnimatedProductCardComponent(BaseProductCardComponent):
    """
    Product card used in ProductListComponents in:
    MainPage, ProductsPage and FilteredProductsPage
    """

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)

    # ACTIONS
    @step_log.log("Open [{self._component_title}]")
    def open(self):
        self._locator.view_product().click()

    @step_log.log("Add to cart from overlay: [{self._component_title}]")
    def add_to_cart_from_overlay(self):
        self.show_overlay()
        self._locator.overlay_add_to_cart().click()

    @step_log.log("Show product card overlay: [{self._component_title}]")
    def show_overlay(self):
        self._locator.product_info().hover(0.5)

    # ASSERTIONS
    @step_log.log("Check [{self._component_title}] has title in overlay: {title}")
    def check_product_has_title_in_overlay(self, title: str):
        self._locator.overlay_title().should_have_text(title)

    @step_log.log("Check [{self._component_title}] has price in overlay: {price}")
    def check_product_has_price_in_overlay(self, price: Price):
        self._locator.overlay_price().should_have_text(price.get_price_text())

    @override
    @step_log.log("Check animated product card has data: [{self._component_title}]")
    def check_product_card_has_data(self, product: Product):
        self.check_product_has_title(product.title)
        self.check_product_has_price(product.price)
        self.check_product_has_title_in_overlay(product.title)
        self.check_product_has_price_in_overlay(product.price)


class _ProductCardComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def product_info(self):
        return UiElement(self.__root.element(".productinfo"), "Product card wrapper")

    def img(self) -> UiElement:
        return self.product_info().element("img", "Product image", UiElement)

    def price(self) -> Text:
        return self.product_info().element("h2", "Product Price", Text)

    def title(self) -> Text:
        return self.product_info().element("p", "Product Title", Text)

    def add_to_cart(self) -> Button:
        return self.product_info().element("a", "Product Add To Cart", Button)

    def overlay(self) -> UiElement:
        return UiElement(self.__root.element(".product-overlay"), "Product Overlay")

    def overlay_title(self) -> Text:
        return self.overlay().element("p", "Overlay Product Title", Text)

    def overlay_price(self) -> Text:
        return self.overlay().element("h2", "Overlay Product Price", Text)

    def overlay_add_to_cart(self) -> Button:
        return self.overlay().element("a", "Overlay Add To Cart", Button)

    def view_product(self) -> Button:
        return Button(self.__root.element(".choose a"), "View Product")
