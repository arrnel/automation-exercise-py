from typing import List, Type, TypeVar, Generic, overload

from selene.core.entity import Element
from selene.support.conditions.have import text

from src.ex.exception import ProductNotFoundError
from src.model.price import Price
from src.model.product_item_info import ProductItemInfo, ProductItemsInfo
from src.ui.component.base_component import BaseComponent
from src.ui.component.product.product_item_component import BaseProductItemComponent
from src.ui.element.base_element import ElementsCollection, UiElement, Text
from src.util import collection_util
from src.util.allure.step_logger import step_log
from src.util.selene.condition import text_in

TBaseProductItemComponent = TypeVar("TBaseProductItemComponent", bound=BaseProductItemComponent)


# class ProductItemsComponent(BaseComponent):
#
#     def __init__(self, root: Element, component_title: str, item_cls: Type[TBaseProductItemComponent], ):
#         super().__init__(root, component_title)
#         self.__locator = _ProductItemsComponentLocator(root)
#         self.__item_cls: type[TBaseProductItemComponent] = item_cls
#
#     # ACTIONS
#     def get_item_by_title(self, title: str) -> TBaseProductItemComponent:
#         item = self.__find_item_by_title(title)
#         if not item:
#             raise ProductNotFoundError(f"Product not found by title: {title}")
#         return item
#
#     def get_items_by_title(self, title: str, *titles: str) -> List[TBaseProductItemComponent]:
#         all_titles = {title, *titles}
#         return [
#             item
#             for item in self.__get_items()
#             if item.get_item_title() in all_titles
#         ]
#
#     def __get_items(self) -> List[TBaseProductItemComponent]:
#         """Returns cards items list"""
#         items = [
#             self.__locator.item_by_title(element.get(query.text))
#             for element in self.__locator.item_titles()
#         ]
#         return [self.__item_cls(ui_element.locator, ui_element.element_title) for ui_element in items]
#
#     def __find_item_by_title(self, title):
#         items = self.__get_items()
#         for item in items:
#             if item.get_title() == title:
#                 return item
#         return None
#
#     # ASSERTIONS
#     def check_cart_is_empty(self):
#         self.__locator.empty_cart().should_be_visible()
#
#     def check_contains_items(self, title: str, *titles: str):
#         all_titles = {title, *titles}
#         with step_log.log(f"Check [{self._component_title}] contains items: {all_titles}"):
#             not_found_items = [
#                 item.get_title()
#                 for item in self.__get_items()
#                 if item.get_title() not in all_titles
#             ]
#
#             if not_found_items:
#                 raise AssertionError(f"Not found item(s) titles: {not_found_items}")
#
#     def check_not_contains_items(self, title: str, *titles: str):
#         all_titles = {title, *titles}
#         with step_log.log(f"Check [{self._component_title}] not contains items: {all_titles}"):
#             found_items = [
#                 item.get_title()
#                 for item in self.__get_items()
#                 if item.get_title() in all_titles
#             ]
#
#             if found_items:
#                 raise AssertionError(f"Found item(s) titles: {found_items}")
#
#     def check_has_items(self, title: str, *titles: str):
#         """Check items in card has products with titles"""
#         all_titles = {title, *titles}
#         with step_log.log(f"Check [{self._component_title}] has items: {all_titles}"):
#             actual_titles = {item.get_product_title() for item in self.__get_items()}
#             not_found_expected, extra_actual = collection_util.remove_common_duplicates(all_titles, actual_titles)
#             if not_found_expected or extra_actual:
#                 raise AssertionError(
#                     "Actual products has diff:\n"
#                     f"Not found product titles: {not_found_expected}\n"
#                     f"Extra product titles: {extra_actual}\n"
#                     f"Expected product titles: {all_titles}\n"
#                     f"Actual product titles: {actual_titles}\n"
#                 )
#
#     def check_visible_component_elements(self) -> None:
#         if not self.__get_items():
#             raise AssertionError("Product items not exists")
#
#     def check_not_visible_component_elements(self) -> None:
#         if self.__get_items():
#             raise AssertionError("Product cards exists")
#
#
# class _ProductItemsComponentLocator:
#
#     def __init__(self, root: Element):
#         self.__root = root
#
#     def empty_cart(self) -> UiElement:
#         return UiElement(self.__root.element("..").element("#empty_cart"), "Empty cart")
#
#     def items(self) -> Collection:
#         return self.__root.all("tr[id^=product]")
#
#     def item_titles(self) -> Collection:
#         return self.__root.all("tr[id^=product] h4 a")
#
#     def item_by_title(self, title: str) -> UiElement:
#         return UiElement(
#             root=self.__root.element(
#                 f"//tr[contains(@id,'product-') and .//a[text()='{title}']]"),
#             element_title=f"Product item '{title}'"
#         )


class ProductItemsComponent(BaseComponent, Generic[TBaseProductItemComponent]):

    def __init__(self, root: Element, component_title: str, cls: Type[TBaseProductItemComponent]):
        super().__init__(root, component_title)
        self.__items = ElementsCollection[TBaseProductItemComponent](
            collection=root.all("tr[id^=product]"),
            collection_title=component_title,
            cls=cls
        )

    # ACTIONS
    def get_item_by_title(self, title: str) -> TBaseProductItemComponent:
        card = self.__items.find_element_by_child(
            child=".cart_description h4 a",
            condition=text(title),
            element_title=f"Product item '{title}'"
        )
        if card is None:
            raise ProductNotFoundError(f"Product item '{title}' not found")
        return card

    def get_items_by_title(self, title: str, *titles: str) -> List[TBaseProductItemComponent]:
        all_titles = {title, *titles}
        return self.__items.filter_by_child(
            child="productinfo p",
            condition=text_in(all_titles),
            collection_title=""
        ).extract()

    # ASSERTIONS
    def check_cart_is_empty(self):
        if len(self.__items):
            raise AssertionError(f"Cart '{self._component_title}' is not empty")

    def check_contains_product_titles(self, title: str, *titles: str):
        all_titles = {title, *titles}
        with step_log.log(f"Check [{self._component_title}] contains product titles: {all_titles}"):
            not_found_items = [
                item.get_title()
                for item in self.__items
                if item.get_title() not in all_titles
            ]

            if not_found_items:
                raise AssertionError(f"Not found item(s) titles: {not_found_items}")

    def check_contains_exact_product_item(self, item: ProductItemInfo):

        with step_log.log(f"Check [{self._component_title}] contains item [{item.title}] with expected data"):

            actual_product_items = {
                ProductItemInfo(
                    id=product_item.get_id(),
                    title=product_item.get_title(),
                    category=product_item.get_category(),
                    price=product_item.get_price(),
                    quantity=product_item.get_quantity(),
                    total_price=product_item.get_total_price(),
                ) for product_item in self.__items}

            product_item = next(
                (i for i in actual_product_items if i.id == item.id),
                None
            )

            if product_item is None:
                raise ProductNotFoundError(f"Product with id = [{item.id}] not found")

            if item != product_item:
                raise AssertionError(f"Found mismatched product item:\n"
                                     f"Expected: {item}\n"
                                     f"Actual: {product_item}")

    def check_contains_exact_product_items(self, product_items: ProductItemsInfo):

        with step_log.log(f"Check [{self._component_title}] contains product items with expected data"):

            actual_product_items = {
                ProductItemInfo(
                    id=product_item.get_id(),
                    title=product_item.get_title(),
                    category=product_item.get_category(),
                    price=product_item.get_price(),
                    quantity=product_item.get_quantity(),
                    total_price=product_item.get_total_price(),
                ) for product_item in self.__items
            }

            mismatch_product_items = {
                item
                for item in product_items.products_info
                if item not in actual_product_items
            }

            if mismatch_product_items:
                raise AssertionError(f"Found mismatched product items: {mismatch_product_items}\n"
                                     f"Expected: {product_items.products_info}\n"
                                     f"Actual: {actual_product_items}")

    def check_not_contains_product_titles(self, title: str, *titles: str):
        all_titles = {title, *titles}
        with step_log.log(f"Check [{self._component_title}] not contains product titles: {all_titles}"):
            found_items = [
                item.get_title()
                for item in self.__items
                if item.get_title() in all_titles
            ]

            if found_items:
                raise AssertionError(f"Found item(s) titles: {found_items}")

    def check_has_product_titles(self, title: str, *titles: str):
        """Check items in card has products with titles"""
        all_titles = {title, *titles}
        with step_log.log(f"Check [{self._component_title}] has items: {all_titles}"):
            actual_titles = {item.get_product_title() for item in self.__items}
            not_found_expected, extra_actual = collection_util.remove_common_duplicates(all_titles, actual_titles)
            if not_found_expected or extra_actual:
                raise AssertionError(
                    "Actual products has diff:\n"
                    f"Not found product titles: {not_found_expected}\n"
                    f"Extra product titles: {extra_actual}\n"
                    f"Expected product titles: {all_titles}\n"
                    f"Actual product titles: {actual_titles}\n"
                )

    @step_log.log("Check all products total price")
    def check_all_products_total_price(self, price: Price):
        total_price_el = Text(self._root.element("p.cart_total_price"), "Total Price")
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
