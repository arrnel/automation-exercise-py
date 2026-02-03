from typing import List, Type, TypeVar, Generic

from selene.core.entity import Element
from selene.support.conditions.have import text

from src.ex.exception import ProductNotFoundError
from src.model.price import Price
from src.model.product_item_info import ProductItemInfo
from src.model.product_items_info import ProductItemsInfo
from src.ui.component.base_component import BaseComponent
from src.ui.component.product.product_item_component import BaseProductItemComponent
from src.ui.element.base_element import ElementsCollection, Text
from src.util import collection_util
from src.util.decorator.step_logger import step_log
from src.util.selene.condition import text_in

TBaseProductItemComponent = TypeVar(
    "TBaseProductItemComponent", bound=BaseProductItemComponent
)
_CART_ITEM_DESCRIPTION_SELECTOR = ".cart_description h4 a"


class ProductItemsComponent(BaseComponent, Generic[TBaseProductItemComponent]):

    def __init__(
        self, root: Element, component_title: str, cls: Type[TBaseProductItemComponent]
    ):
        super().__init__(root, component_title)
        self.__items = ElementsCollection[TBaseProductItemComponent](
            collection=root.all("tr[id^=product]"),
            collection_title=component_title,
            cls=cls,
        )

    # ACTIONS
    def get_item_by_title(self, title: str) -> TBaseProductItemComponent:
        card = self.__items.find_element_by_child(
            child=_CART_ITEM_DESCRIPTION_SELECTOR,
            condition=text(title),
            element_title=f"Product item '{title}'",
        )
        if card is None:
            raise ProductNotFoundError(f"Product item '{title}' not found")
        return card

    def get_items_by_title(
        self, title: str, *titles: str
    ) -> List[TBaseProductItemComponent]:
        all_titles = {title, *titles}
        return self.__items.filter_by_child(
            child=_CART_ITEM_DESCRIPTION_SELECTOR,
            condition=text_in(all_titles),
            collection_title="",
        ).extract(selector_to_extract_component_title=_CART_ITEM_DESCRIPTION_SELECTOR)

    # ASSERTIONS
    def check_cart_is_empty(self):
        if len(self.__items):
            raise AssertionError(f"Cart '{self._component_title}' is not empty")

    def check_contains_product_titles(self, title: str, *titles: str):
        all_expected_titles = {title, *titles}
        with step_log.log(
            f"Check [{self._component_title}] contains product titles: {all_expected_titles}"
        ):
            all_actual_titles = [item.get_title() for item in self.__items]

            not_found_items = [
                item_title
                for item_title in all_expected_titles
                if item_title not in all_actual_titles
            ]

            if not_found_items:
                raise AssertionError(f"Not found item(s) titles: {not_found_items}")

    def check_contains_exact_product_item(self, item: ProductItemInfo):

        with step_log.log(
            f"Check [{self._component_title}] contains item [{item.title}] with expected data"
        ):

            actual_product_items = {
                ProductItemInfo(
                    id=product_item.get_id(),
                    title=product_item.get_title(),
                    category=product_item.get_category(),
                    price=product_item.get_price(),
                    quantity=product_item.get_quantity(),
                    total_price=product_item.get_total_price(),
                )
                for product_item in self.__items
            }

            product_item = next(
                (i for i in actual_product_items if i.id == item.id), None
            )

            if product_item is None:
                raise ProductNotFoundError(f"Product with id = [{item.id}] not found")

            if item != product_item:
                raise AssertionError(
                    f"Found mismatched product item:\n"
                    f"Expected: {item}\n"
                    f"Actual: {product_item}"
                )

    @step_log.log(
        "Check [{self._component_title}] contains product items with expected data"
    )
    def check_contains_exact_product_items(self, product_items: ProductItemsInfo):

        actual_product_items = [
            ProductItemInfo(
                id=product_item.get_id(),
                title=product_item.get_title(),
                category=product_item.get_category(),
                price=product_item.get_price(),
                quantity=product_item.get_quantity(),
                total_price=product_item.get_total_price(),
            )
            for product_item in self.__items
        ]

        mismatch_product_items = [
            item
            for item in product_items.products_info
            if item not in actual_product_items
        ]

        if mismatch_product_items:
            raise AssertionError(
                f"Found mismatched product items: {mismatch_product_items}\n"
                f"Expected: {product_items.products_info}\n"
                f"Actual: {actual_product_items}"
            )

    def check_not_contains_product_titles(self, title: str, *titles: str):
        all_expected_titles = {title, *titles}
        with step_log.log(
            f"Check [{self._component_title}] not contains product titles: {all_expected_titles}"
        ):
            all_actual_titles = [item.get_title() for item in self.__items]
            found_items = [
                title for title in all_expected_titles if title in all_actual_titles
            ]

            if found_items:
                raise AssertionError(f"Found item(s) titles: {found_items}")

    def check_has_product_titles(self, title: str, *titles: str):
        """Check items in card has products with titles"""
        all_expected_titles = {title, *titles}
        with step_log.log(
            f"Check [{self._component_title}] has items: {all_expected_titles}"
        ):
            all_actual_titles = [item.get_title() for item in self.__items]
            not_found_expected, extra_actual = collection_util.remove_common_duplicates(
                all_expected_titles, all_actual_titles
            )
            if not_found_expected or extra_actual:
                raise AssertionError(
                    "Actual products has diff:\n"
                    f"Not found product titles: {not_found_expected}\n"
                    f"Extra product titles: {extra_actual}\n"
                    f"Expected product titles: {all_expected_titles}\n"
                    f"Actual product titles: {all_actual_titles}\n"
                )

    @step_log.log("Check all products total price")
    def check_all_products_total_price(self, price: Price):
        total_price_el = Text(
            self._root.element("td:not(.cart_total) p.cart_total_price"),
            "Total Price",
        )
        total_price_el.should_have_text(price.get_price_text())

    def check_checkout_table_data(self, items_info: ProductItemsInfo):
        self.check_contains_exact_product_items(items_info)
        self.check_all_products_total_price(items_info.total_price)

    def check_visible_component_elements(self) -> None:
        if not self.__items:
            raise AssertionError("Product items not exists")

    def check_not_visible_component_elements(self) -> None:
        if self.__items:
            raise AssertionError("Product cards exists")
