from typing import List, Type, Optional

from selene import be
from selene.core.entity import Element

from src.ui.component.base_component import BaseComponent, create_instance_of_base_component
from src.ui.component.product.product_item_component import BaseProductItem, ProductItemComponent
from src.util.list_util import concat_args
from src.util.step_logger import step_log


class ProductItemsComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str, cls: Type[BaseProductItem]):
        super().__init__(root, component_title)
        self.__cls = cls

    # ASSERTIONS
    def check_cart_is_empty(self):
        self._root.element("..").element("#empty_cart").should(be.visible)

    @step_log.log()
    def check_contains_items(self, title: str, *titles: str):
        all_titles = concat_args(title, *titles)
        not_found_items = [
            product.get_item_title()
            for product in self.__get_items()
            if product.get_item_title() not in all_titles
        ]

        if not_found_items:
            raise AssertionError("Not found item(s) titles: ")

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

    def get_items_by_title(self, title:str, *titles: str) -> List[ProductItemComponent]:
        all_titles = concat_args(title, *titles)
        return (
            []
            if not all_titles else
            [
                item
                for item in self.__get_items()
                if item.get_item_title() in all_titles
            ]
        )

    def check_visible_component_elements(self) -> None:
        pass

    def check_not_visible_component_elements(self) -> None:
        pass
