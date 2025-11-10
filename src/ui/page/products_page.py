from typing import override

from selene import browser

from src.ui.component.filter_component import AccordionFilter, CategoryStatFilter, SearchFilter
from src.ui.component.product.product_card_component import AnimatedProductCard
from src.ui.component.product.products_collection_component import ProductCardsComponent
from src.ui.page.base_page import BasePage
from src.util.step_logger import step_log


class ProductsPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__search_filter = SearchFilter(self._page_container.element("#advertisement .container"), "Search filter")
        self.__category_filter = AccordionFilter(self._page_container.element(".left-sidebar #accordian"), "Category filter")
        self.__products = ProductCardsComponent(self._page_container.element(".features_items"), "Features Items", cls=AnimatedProductCard)
        self.__brand_filter = CategoryStatFilter(self._page_container.element(".left-sidebar .brands-name"), "Brand filter")

    # COMPONENTS
    @property
    def search_filter(self) -> SearchFilter:
        return self.__search_filter

    @property
    def category_filter(self) -> AccordionFilter:
        return self.__category_filter

    @property
    def brand_filter(self) -> CategoryStatFilter:
        return self.__brand_filter

    @property
    def products(self) -> ProductCardsComponent:
        return self.__products

    # ACTIONS
    @step_log.log("Open: /products")
    def navigate(self) -> None:
        browser.open("/")

    # ASSERTIONS
    @override
    @step_log.log("Check [{self._page_name}] is visible")
    def check_page_is_visible(self):
        self.__search_filter.check_component_is_visible()

    @override
    @step_log.log("Check [{self._page_name}] is not visible")
    def check_page_is_not_visible(self):
        self.__search_filter.check_component_is_not_exists()
