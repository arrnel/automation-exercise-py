from typing import List, Type, Optional

from selene import be
from selene.core.entity import Element

from src.ui.component.base_component import BaseComponent, create_instance_of_base_component
from src.ui.component.product.product_card_component import (
    ProductCard,
    AnimatedProductCard,
    BaseProductCard,
    ProductItemComponent,
    BaseProductItem,
)


class ProductCardsComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str, cls: Type[BaseProductCard]):
        super().__init__(root, component_title)
        self.__cls = cls

    def __get_cards(self) -> List[AnimatedProductCard]:
        """Returns cards list"""
        cards = []
        for i, el in enumerate(self._root.all(".product-card")):  # .product-card — общий CSS
            card = create_instance_of_base_component(self.__cls, el, "")
            card._change_component_title(f"Product card [{card.get_product_title()}]")
            cards.append(card)
        return cards

    def get_card_by_title(self, title: str) -> Optional[AnimatedProductCard]:
        """Возвращает карточку по названию товара."""
        cards = self.__get_cards()
        for card in cards:
            if card.get_product_title() == title:
                return card
        return None

    def get_cards_by_title(self, *args: str) -> List[ProductCard]:
        cards = []
        for card in self.__get_cards():
            card_title = card.get_product_title()
            if card_title in args:
                cards.append(card)
        return cards

    def check_contains_products(self, *args: str):
        not_found_cards = []
        for card in self.__get_cards():
            card_title = card.get_product_title()
            if card_title not in args:
                not_found_cards.append(card_title)
        if not not_found_cards:
            raise AssertionError(f"Not found product cards: {not_found_cards}")

    def check_products_quantity(self, quantity: int):
        actual_products_quantity = len(self.__get_cards())
        if quantity != actual_products_quantity:
            raise AssertionError(
                f"Expected and actual products count not equals. Expected = [{quantity}], actual = [{actual_products_quantity}]"
            )

    def check_visible_component_elements(self) -> None:
        if not self.__get_cards():
            raise AssertionError("Product cards not exists")

    def check_not_visible_component_elements(self) -> None:
        if self.__get_cards():
            raise AssertionError("Product cards exists")


class ProductListComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str, cls: Type[BaseProductItem]):
        super().__init__(root, component_title)
        self.__cls = cls

    def check_cart_is_empty(self):
        self._root.element("..").element("#empty_cart").should(be.visible)

    def __get_items(self) -> List[ProductItemComponent]:
        """Returns cards list"""
        cards = []
        for i, el in enumerate(self._root.all(".product-card")):  # .product-card — общий CSS
            card = create_instance_of_base_component(self.__cls, el, "")
            card._change_component_title(f"Product card [{card.get_title()}]")
            cards.append(card)
        return cards

    def get_item_by_title(self, title: str) -> Optional[ProductItemComponent]:
        """Возвращает карточку по названию товара."""
        cards = self.__get_items()
        for card in cards:
            if card.get_title() == title:
                return card
        return None

    def get_items_by_title(self, *args: str) -> List[ProductItemComponent]:
        cards = []
        for card in self.__get_items():
            card_title = card.get_title()
            if card_title in args:
                cards.append(card)
        return cards

    def check_visible_component_elements(self) -> None:
        pass

    def check_not_visible_component_elements(self) -> None:
        pass
