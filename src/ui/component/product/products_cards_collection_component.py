from typing import List, TypeVar, Type, Generic

from selene import Element
from selene.support.conditions.have import text

from src.ex.exception import ProductNotFoundError
from src.ui.component.base_component import BaseComponent
from src.ui.component.product.product_card_component import BaseProductCardComponent
from src.ui.element.base_element import ElementsCollection
from src.util import collection_util
from src.util.decorator.step_logger import step_log
from src.util.selene.condition import text_in

TBaseProductCardComponent = TypeVar(
    "TBaseProductCardComponent", bound=BaseProductCardComponent
)


class ProductCardsComponent(BaseComponent, Generic[TBaseProductCardComponent]):

    def __init__(
        self,
        root: Element,
        component_title: str,
        cls: Type[TBaseProductCardComponent],
    ):
        super().__init__(root, component_title)
        self.__cards = ElementsCollection[TBaseProductCardComponent](
            collection=root.all(".product-image-wrapper"),
            collection_title=component_title,
            cls=cls,
        )

    def get_card_by_title(self, title: str) -> TBaseProductCardComponent:
        card = self.__cards.find_element_by_child(
            child=".productinfo p",
            condition=text(title),
            element_title=f"{title}",
        )
        if card is None:
            raise ProductNotFoundError(f"Product card '{title}' not found")
        return card

    def get_cards_by_title(
        self,
        title: str,
        *titles: str,
        collection_title: str = "",
    ) -> List[TBaseProductCardComponent]:
        all_titles = {title, *titles}
        return self.__cards.filter_by_child(
            child=".productinfo p",
            condition=text_in(all_titles),
            collection_title=collection_title,
        ).extract(selector_to_extract_component_title="p")

    # ASSERTIONS
    @step_log.log("Check {self._component_title} is empty")
    def check_catalog_is_empty(self):
        if len(self.__cards):
            raise AssertionError(
                f"Products catalog '{self._component_title}' is not empty"
            )

    def check_contains_products(self, title: str, *titles: str):
        all_titles = {title, *titles}
        with step_log.log(
            f"Check {self._component_title} contains products: {all_titles}"
        ):
            not_found_cards = [
                card.get_product_title()
                for card in self.__cards
                if card.get_product_title() not in all_titles
            ]
            if not_found_cards:
                raise AssertionError(f"Not found product cards: {not_found_cards}")

    def check_not_contains_products(self, title: str, *titles: str):
        all_titles = {title, *titles}
        with step_log.log(
            f"Check {self._component_title} not contains products: {all_titles}"
        ):
            found_cards = [
                card.get_product_title()
                for card in self.__cards
                if card.get_product_title() in all_titles
            ]
            if found_cards:
                raise AssertionError(f"Found product cards: {found_cards}")

    def check_has_products(self, title: str, *titles: str):
        all_titles = {title, *titles}
        with step_log.log(
            f"Check [{self._component_title}] has products: {all_titles}"
        ):
            actual_titles = {card.get_product_title() for card in self.__cards}
            not_found_expected, extra_actual = collection_util.remove_common_duplicates(
                all_titles, actual_titles
            )
            if not_found_expected or extra_actual:
                raise AssertionError(
                    "Actual products has diff:\n"
                    f"Not found product titles: {not_found_expected}\n"
                    f"Extra product titles: {extra_actual}\n"
                    f"Expected product titles: {all_titles}\n"
                    f"Actual product titles: {actual_titles}\n"
                )

    @step_log.log("Check [{self._component_title}] has products count: {count}")
    def check_has_products_count(self, count: int):
        if count <= 0:
            raise ValueError(
                f"Product count must be greater then 0. Actual count = {count}"
            )

        actual_products_quantity = len(self.__cards)
        if count != actual_products_quantity:
            raise AssertionError(
                "Expected and actual products count not equals. "
                f"Expected = [{count}], "
                f"Actual = [{actual_products_quantity}]"
            )

    def check_visible_component_elements(self) -> None:
        if not self.__cards:
            raise AssertionError("Product cards not exists")

    def check_not_visible_component_elements(self) -> None:
        if self.__cards:
            raise AssertionError("Product cards exists")
