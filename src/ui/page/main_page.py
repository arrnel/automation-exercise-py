from typing import override

from selene import browser

from src.ui.component.carousel_component import (
    ImageCarouselComponent,
    ProductCarouselComponent,
)
from src.ui.component.filter_component import AccordionFilter, CategoryStatFilter
from src.ui.component.product.product_card_component import AnimatedProductCardComponent
from src.ui.component.product.products_cards_collection_component import (
    ProductCardsComponent,
)
from src.ui.page.base_page import BasePage
from src.util.decorator.step_logger import step_log

URL = "/"


class MainPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__banner = ImageCarouselComponent(
            root=self._page_container.element("#slider-carousel"),
            component_title="Images banner",
        )
        self.__category_filter = AccordionFilter(
            root=self._page_container.element(".left-sidebar #accordian"),
            component_title="Category filter",
        )
        self.__products = ProductCardsComponent[AnimatedProductCardComponent](
            root=self._page_container.element(".features_items"),
            component_title="Features Items",
            cls=AnimatedProductCardComponent,
        )
        self.__brand_filter = CategoryStatFilter(
            root=self._page_container.element(".left-sidebar .brands-name"),
            component_title="Brand filter",
        )
        self.__recommended_products = ProductCarouselComponent(
            root=self._page_container.element(".recommended_items"),
            component_title="Recommended products",
        )

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
    def products(self) -> ProductCardsComponent[AnimatedProductCardComponent]:
        return self.__products

    @property
    def recommended_products(self) -> ProductCarouselComponent:
        return self.__recommended_products

    # ACTIONS
    @step_log.log("Open [Main Page]: {URL}")
    def navigate(self) -> None:
        browser.open(URL)

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
