import time
from abc import ABC
from typing import Optional, List

from selene import Element, be, query, have
from selene.support.conditions.be import not_, existing

from src.ui.component.base_component import BaseComponent
from src.ui.component.product.product_card_component import ProductCardComponent
from src.ui.element.base_element import UiElement, ElementsCollection
from src.util.allure.step_logger import step_log
from src.util.string_util import StringUtil

_PRODUCT_CONTAINER_SELECTOR: str = "//div[contains(@class,'productInfo') and text()='%s']"
_CAROUSEL_SCROLL_TIMEOUT: int = 1_000


class BaseCarouselComponent(BaseComponent, ABC):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self._locator = _CarouselComponentLocator(root)
        self._component_title = StringUtil.camel_case_to_normal(type(self).__name__)

    # ACTIONS
    @step_log.log("Show previous [{self._component_title}] slide")
    def previous(self) -> None:
        self._locator.previous().click()
        time.sleep(_CAROUSEL_SCROLL_TIMEOUT)

    @step_log.log("Show next [{self._component_title}] slide")
    def next(self) -> None:
        self._locator.next().click()
        time.sleep(_CAROUSEL_SCROLL_TIMEOUT)

    @step_log.log("Waiting for expected [{self._component_title}] slide will be active")
    def wait_until_slide_will_be_active(self, slide_number: int):
        all_slides = self._locator.carousel_slides()
        all_slides_count = len(all_slides)
        if slide_number < 0 or slide_number > all_slides_count - 1:
            raise ValueError(
                f"Slide number can not be negative or be greater then all slides count - 1.\n"
                f"Slide number: {slide_number},\n"
                f"Available slide numbers: 0,..,{all_slides_count - 1}"
            )

        attempts = all_slides_count
        while attempts > 0:
            if slide_number == self._get_active_slide_number():
                return self
            if attempts <= all_slides_count - attempts:
                self.previous()
            else:
                self.next()
            attempts -= 1
            time.sleep(_CAROUSEL_SCROLL_TIMEOUT)

        raise RuntimeError(f"Slide number {slide_number} not found")

    # ASSERTIONS
    @step_log.log("Check active slide number of [{self._component_title}] equals: {slide_number}")
    def check_active_slide_number_equals(self, slide_number: int) -> None:
        if slide_number < 0:
            raise ValueError("Slide number cannot be negative")
        assert self._get_active_slide_number() == slide_number, "Check carousel active slide number equals"

    def _get_active_slide_number(self) -> int:
        slides = self._locator.carousel_slides()
        for i, slide in enumerate(slides):
            if "active" in slide.get(query.attribute("class")):
                return i
        return -1

    @step_log.log("Check component [{self._component_title}] is visible")
    def check_component_is_visible(self) -> None:
        self._root.should(be.visible)

    @step_log.log("Check component [{self._component_title}] is not exists")
    def check_component_is_not_exists(self) -> None:
        self._root.should(not_.visible)


class ImageCarouselComponent(BaseCarouselComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)

    # ASSERTIONS
    @step_log.log("Check component [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self._locator.previous().should(be.visible)
        self._locator.next().should(be.visible)
        self._locator.active_carousel_slide().should(be.visible)

    @step_log.log("Check component [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self._locator.previous().should(not_.existing)
        self._locator.next().should(not_.existing)
        self._locator.active_carousel_slide().should(not_.existing)


class ProductCarouselComponent(BaseCarouselComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)

    # ACTIONS
    def get_card_by_title(self, title: str) -> ProductCardComponent:
        card_element = self._locator.carousel_product(title)
        return ProductCardComponent(
            root=card_element.locator,
            component_title=f"Product card '{title}'",
        )

    def get_active_card_by_title(self, title: str) -> ProductCardComponent:
        self.found_product(title)
        return self.get_card_by_title(title)

    @step_log.log("Add products to cart: {*args}")
    def add_products_to_cart(self, *args: str) -> None:
        for product_title in args:
            self.add_product_to_cart(product_title)

    @step_log.log("Add product to cart: {product_title}")
    def add_product_to_cart(self, product_title: str) -> None:
        product = self.scroll_to_product(product_title)
        if not product:
            raise RuntimeError(f"Product with title = [{product_title}] not found in carousel")
        self._locator.add_to_cart(product_title).click()

    def scroll_to_product(self, product_title: str) -> Optional[Element]:
        return self.found_product(product_title)

    # ASSERTIONS
    @step_log.log("Check [{self._component_title}] contains product with title: {product_title}")
    def check_contains_product(self, product_title: str) -> None:
        if not self.found_product(product_title):
            raise AssertionError(f"Product with title = [{product_title}] not found in carousel")

    @step_log.log("Check [{self._component_title}] contains expected products: {product_titles}")
    def check_contains_products(self, product_titles: List[str]):
        not_found_products = [title for title in product_titles if not self.found_product(title)]
        if not_found_products:
            raise AssertionError(f"Product carousel expected products not found: {not_found_products}")

    @step_log.log("Check product [{product_title}] has price: {price}")
    def check_product_has_price(self, product_title: str, price) -> None:
        product = self.found_product(product_title)
        if not product:
            raise RuntimeError(f"Product with title = [{product_title}] not found in carousel")
        product.element("h2").should(have.text(price.get_price_text()))

    def found_product(self, product_title: str) -> Optional[Element]:
        return Optional[
            self._locator.carousel_slides().find_element_by_child(
                child="p",
                condition=have.text(product_title),
                element_title=f"Carousel product '{product_title}'",
            )
        ]

    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self._locator.previous().should(be.visible)
        self._locator.next().should(be.visible)
        self._locator.active_carousel_slide().should(be.visible)

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self._locator.previous().should(not_.existing)
        self._locator.next().should(not_.existing)
        self._locator.active_carousel_slide().should(not_.existing)


class _CarouselComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def carousel_inner(self) -> UiElement:
        return UiElement(self.__root.element(".carousel-inner"), "")

    def active_carousel_slide(self) -> UiElement:
        return UiElement(self.__root.element(".item.active"), "Active carousel slide")

    def carousel_slides(self) -> ElementsCollection:
        return ElementsCollection[ProductCarouselComponent](self.__root.all(".item"), "Carousel Slides", ProductCarouselComponent)

    def carousel_product(self, product_title: str) -> UiElement:
        return self.carousel_slides().find_element_by_child(
            child=_PRODUCT_CONTAINER_SELECTOR.format(product_title),
            condition=existing,
            element_title=f"Carousel Product '{product_title}'",
        )

    def active_carousel_product(self, product_title: str) -> UiElement:
        return self.active_carousel_slide().element(
            css_or_xpath_or_by=_PRODUCT_CONTAINER_SELECTOR.format(product_title),
            element_title=f"Product '{product_title}' in active carousel"
        )

    def add_to_cart(self, product_title: str):
        return self.__root.element(f"//div[contains(@class,'productinfo') and ./p[text()='{product_title}']]").element(
            ".add-to-cart")

    def previous(self) -> Element:
        return self.__root.element("a[data-slide=prev]")

    def next(self) -> Element:
        return self.__root.element("a[data-slide=next]")
