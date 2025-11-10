from typing import override

import allure
from selene import browser

from src.ui.component.carousel_component import ImageCarouselComponent, ProductCarouselComponent
from src.ui.component.filter_component import AccordionFilter, CategoryStatFilter
from src.ui.component.product.product_card_component import AnimatedProductCard
from src.ui.component.product.products_collection_component import ProductCardsComponent
from src.ui.page.base_page import BasePage
from src.util.step_logger import step_log


class MainPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__banner = ImageCarouselComponent(self._page_container.element("#slider-carousel"), "Images banner")
        self.__category_filter = AccordionFilter(self._page_container.element(".left-sidebar #accordian"), "Category filter")
        self.__products = ProductCardsComponent(self._page_container.element(".features_items"), "Features Items", cls=AnimatedProductCard)
        self.__brand_filter = CategoryStatFilter(self._page_container.element(".left-sidebar .brands-name"), "Brand filter")
        self.__recommended_products = ProductCarouselComponent(self._page_container.element(".recommended_items"), "Recommended products")

    # COMPONENTS
    @property
    def banner(self) -> ImageCarouselComponent:
        return self.__banner

    @property
    def category_filter(self) -> AccordionFilter:
        return self.__category_filter

    @property
    def brand_filter(self) -> CategoryStatFilter:
        return self.__brand_filter

    @property
    def products(self) -> ProductCardsComponent:
        return self.__products

    @property
    def recommended_products(self) -> ProductCarouselComponent:
        return self.__recommended_products

    # ACTIONS
    def navigate(self) -> None:
        with allure.step("Open: /"):
            browser.open("/")

    # ASSERTIONS
    @override
    @step_log.log("Check [{self._page_name}] is visible")
    def check_page_is_visible(self):
        self.__banner.check_component_is_visible()
        self.__recommended_products.check_component_is_visible()

    @override
    @step_log.log("Check [{self._page_name}] is not visible")
    def check_page_is_not_visible(self):
        self.__banner.check_component_is_not_exists()
        self.__recommended_products.check_component_is_not_exists()
