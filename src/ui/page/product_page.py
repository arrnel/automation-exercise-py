from typing import override

from selene import browser

from src.ui.component.filter_component import AccordionFilter, CategoryStatFilter
from src.ui.component.product.product_details_component import ProductDetailsComponent
from src.ui.component.review_component import ReviewComponent
from src.ui.page.base_page import BasePage
from src.util.decorator.step_logger import step_log

URL_PATTERN = "/product_details/{product_id}"


class ProductPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__category_filter = AccordionFilter(
            self._page_container.element(".left-sidebar #accordian"), "Category filter"
        )
        self.__brand_filter = CategoryStatFilter(
            self._page_container.element(".left-sidebar .brands-name"), "Brand filter"
        )
        self.__product_details_component = ProductDetailsComponent(
            self._page_container.element(".product-details"), "Product Details"
        )
        # Not provide "#reviews" as locator. Cause #reviews container has height = 0.
        # Illegal for screenshot tests
        self.__review_component = ReviewComponent(
            self._page_container.element(".shop-details-tab"), "Review"
        )

    # COMPONENTS
    @property
    def category_filter(self) -> AccordionFilter:
        return self.__category_filter

    @property
    def brand_filter(self) -> CategoryStatFilter:
        return self.__brand_filter

    @property
    def product_details(self) -> ProductDetailsComponent:
        return self.__product_details_component

    @property
    def review(self) -> ReviewComponent:
        return self.__review_component

    # ACTIONS
    @step_log.log(
        "Open [Product Page]: /product_details/{URL_PATTERN.format(product_id=product_id)}"
    )
    def navigate(self, product_id: int) -> None:
        browser.open(URL_PATTERN.format(product_id=product_id))

    # ASSERTIONS
    @override
    @step_log.log("Check [{self._page_name}] is visible")
    def check_page_is_visible(self):
        self.__product_details_component.check_component_is_visible()
        self.__review_component.check_component_is_visible()

    @override
    @step_log.log("Check [{self._page_name}] is not visible")
    def check_page_is_not_visible(self):
        self.__product_details_component.check_component_is_not_exists()
        self.__review_component.check_component_is_not_exists()
