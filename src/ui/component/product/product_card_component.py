from typing import Optional, override

from selene import Element

from src.model.price import PriceDTO
from src.model.product import ProductDTO
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Button, Text, UiElement, Input
from src.util.step_logger import step_log

_DEFAULT_TIMEOUT_OVERLAY_WAIT = 0.2


class BaseProductCard(BaseComponent):

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)
        self._locator = _ProductCardComponentLocator(self._root)

    def get_product_title(self) -> str:
        return self._locator.title().get_text()

    @step_log.log("Open [{self._component_title}]")
    def add_to_cart(self) -> None:
        self._locator.add_to_cart().click()

    @step_log.log("Check [{self._component_title}] has title: {title}")
    def check_product_has_title(self, title: str) -> None:
        self._locator.title().should_have_text(title)

    @step_log.log("Check [{self._component_title}] has price: {price}")
    def check_product_has_price(self, price: PriceDTO) -> None:
        self._locator.price().should_have_text(price.get_price_text())

    @step_log.log("Check [{self._component_title}] has data")
    def check_product_card_has_data(self, product: ProductDTO) -> None:
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


class ProductCard(BaseProductCard):
    """Product card used in carousel"""

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)


class AnimatedProductCard(BaseProductCard):
    """Product card used in ProductListComponents in MainPage, ProductsPage and FilteredProductsPage"""

    def __init__(self, root: Element, component_title: str = Optional[None]):
        super().__init__(root, component_title)

    # ACTIONS
    @step_log.log("Open [{self._component_title}]")
    def open(self):
        self._locator.view_product().click()

    @step_log.log("Add to cart from overlay: [{self._component_title}]")
    def add_to_cart_from_overlay(self):
        self._locator.overlay_add_to_cart()

    # ASSERTIONS
    @step_log.log("Check [{self._component_title}] has title in overlay: {title}")
    def check_product_has_title_in_overlay(self, title: str):
        self._locator.overlay_title().should_have_text(title)

    @step_log.log("Check [{self._component_title}] has price in overlay: {price}")
    def check_product_has_price_in_overlay(self, price: PriceDTO):
        self._locator.overlay_price().should_have_text(price.get_price_text())

    @step_log.log("Check [{self._component_title}] has overlay screenshot")
    def check_product_overlay_has_screenshot(
        self,
        path_to_screenshot: str,
        percent_of_tolerance: float = 0,
        rewrite_screenshot: bool = False,
    ):
        self._locator.img().hover()
        self._check_element_have_screenshot(
            self._locator.overlay().get_locator(),
            path_to_screenshot,
            percent_of_tolerance,
            rewrite_screenshot,
        )

    @override
    @step_log.log("Check animated product card has data: [{self._component_title}]")
    def check_product_card_has_data(self, product: ProductDTO):
        self.check_product_has_title(product.title)
        self.check_product_has_price(product.price)
        self.check_product_has_title_in_overlay(product.title)
        self.check_product_has_price_in_overlay(product.price)


class BaseProductItem(BaseComponent):

    def __init__(
        self,
        root: Element,
        component_title: str = Optional[None],
        item_title: str = Optional[None],
    ):
        super().__init__(root, component_title)
        self._item_title = item_title
        self._locator = _ProductItemComponentLocator(self._root)

    def get_price(self) -> PriceDTO:
        return PriceDTO.from_text(self._locator.price().get_text())

    def get_title(self) -> str:
        return self._locator.title().get_text()

    def get_total_price(self) -> PriceDTO:
        return PriceDTO.from_text(self._locator.total_price().get_text())

    @step_log.log("Check [{self._item_title}] has price: {price}")
    def should_have_price(self, price: PriceDTO) -> None:
        self._locator.price().should_have_text(price.get_amount_text())

    @step_log.log("Check [{self._item_title}] has quantity: {quantity}")
    def should_have_quantity(self, quantity: int) -> None:
        self._locator.quantity().should_have_value(quantity)

    @step_log.log("Check [{self._item_title}] has total price: {total_price}")
    def should_have_total_price(self, total_price: PriceDTO) -> None:
        self._locator.total_price().should_have_text(total_price.get_amount_text())

    @step_log.log("Check [{self._item_title}] has correct data")
    def should_have_data(
        self, price: PriceDTO, quantity: int, total_price: PriceDTO
    ) -> None:
        self.should_have_price(price)
        self.should_have_quantity(quantity)
        self.should_have_total_price(total_price)


class ProductItemComponent(BaseProductItem):
    """Product card in products list in Checkout"""

    def __init__(
        self,
        root: Element,
        component_title: str = Optional[None],
        item_title: str = Optional[None],
    ):
        super().__init__(root, component_title, item_title)

    def get_item_title(self) -> str:
        return self._locator.title().get_text()

    def get_item_category(self) -> dict[str, str]:
        values = self._locator.category().get_text().split(" > ")
        return {"group": values[0], "category": values[1]}

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
    """Product card in products list in CartPage"""

    def __init__(
        self,
        root: Element,
        component_title: str = Optional[None],
        item_title: str = Optional[None],
    ):
        super().__init__(root, component_title)
        self.__locator = _ProductItemComponentLocator(self._root)

    @step_log.log("Remove [{self._item_title}] from [{self._component_title}]")
    def remove(self):
        self.__locator.remove().click()

    def check_visible_component_elements(self) -> None:
        self.__locator.img().should_be_visible()
        self.__locator.title().should_be_visible()
        self.__locator.price().should_be_visible()
        self.__locator.total_price().should_be_visible()
        self.__locator.quantity().should_be_visible()
        self.__locator.remove().should_be_visible()

    def check_not_visible_component_elements(self) -> None:
        self.__locator.img().should_not_exists()
        self.__locator.title().should_not_exists()
        self.__locator.price().should_not_exists()
        self.__locator.total_price().should_not_exists()
        self.__locator.quantity().should_not_exists()
        self.__locator.remove().should_not_exists()


class _ProductCardComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def img(self) -> UiElement:
        return UiElement(self.__root.element(".productinfo img"), "Product image")

    def price(self) -> Text:
        return Text(self.__root.element("h2"), "Product Price")

    def title(self) -> Text:
        return Text(self.__root.element(".productinfo p"), "Product Title")

    def add_to_cart(self) -> Button:
        return Button(self.__root.element(".productinfo a"), "Product Add To Cart")

    def overlay(self) -> UiElement:
        return UiElement(self.__root.element(".product-overlay"), "Product Overlay")

    def overlay_title(self):
        return Text(self.__root.element("product-overlay p"), "Overlay Product Title")

    def overlay_price(self):
        return Text(self.__root.element("product-overlay h2"), "Overlay Product Price")

    def overlay_add_to_cart(self):
        return Text(self.__root.element("product-overlay a"), "Overlay Add To Cart")

    def view_product(self) -> Button:
        return Button(self.__root.element(".choose a"), "View Product")


class _ProductItemComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def img(self) -> UiElement:
        return UiElement(self.__root.element(".cart_product img"), "Product Image")

    def title(self) -> Text:
        return Text(self.__root.element(".cart_description h4 a"), "Product Title")

    def category(self) -> Text:
        return Text(self.__root.element(".cart_description p"), "Product Category")

    def price(self) -> Text:
        return Text(self.__root.element(".cart_price p"), "Product Price")

    def quantity(self) -> Input:
        return Input(self.__root.element(".cart_quantity button"), "Product Quantity")

    def total_price(self) -> Text:
        return Text(self.__root.element(".cart_total_price p"), "Product Total Price")

    def remove(self) -> Button:
        return Button(self.__root.element(".cart_delete"), "Product Remove")
