import time
from abc import ABC
from typing import Optional, List

from selene import Element, be, have
from selene.support.conditions.be import not_
from selene.support.conditions.have import css_class

from src.ex.exception import ProductNotFoundError
from src.ui.component.base_component import BaseComponent
from src.ui.component.product.product_card_component import ProductCardComponent
from src.ui.element.base_element import UiElement, ElementsCollection, Button
from src.util.decorator.step_logger import step_log
from src.util.string_util import StringUtil

_PRODUCT_CONTAINER_SELECTOR: str = (
    "//div[contains(@class, 'productinfo')]//p[text()='%s']"
)
_CAROUSEL_SCROLL_TIMEOUT: float = 0.5


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
    def wait_until_slide_will_be_active(self, slide_number: int) -> None:
        slide_idx = slide_number - 1
        all_slides = self._locator.carousel_slides()
        slides_count = len(all_slides)

        if slide_idx < 0 or slide_idx >= slides_count:
            raise ValueError(
                f"Slide number must be in range 1..{slides_count}. "
                f"Got: {slide_number}"
            )

        current_slide = self._get_active_slide_number()

        if current_slide == slide_idx:
            return

        forward_steps = (slide_idx - current_slide) % slides_count
        backward_steps = (current_slide - slide_idx) % slides_count

        if forward_steps <= backward_steps:
            step_action = self.next
            steps_to_do = forward_steps
        else:
            step_action = self.previous
            steps_to_do = backward_steps

        for _ in range(steps_to_do):
            step_action()
            time.sleep(_CAROUSEL_SCROLL_TIMEOUT)

            if self._get_active_slide_number() == slide_idx:
                return

        raise RuntimeError(
            f"Failed to activate slide {slide_number}. "
            f"Last active slide: {
                -1
                if self._get_active_slide_number() == -1
                else self._get_active_slide_number() + 1
            }"
        )

    # ASSERTIONS
    @step_log.log(
        "Check active slide number of [{self._component_title}] equals: {slide_number}"
    )
    def check_active_slide_number_equals(self, slide_number: int) -> None:
        if slide_number < 0:
            raise ValueError("Slide number cannot be negative")
        assert (
            self._get_active_slide_number() == slide_number
        ), "Check carousel active slide number equals"

    def _get_active_slide_number(self) -> int:
        slides = self._locator.carousel_slides()
        for i, slide in enumerate(slides):
            if slide.matching(css_class("active")):
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
        product_card = self.found_product(title)
        if not product_card:
            raise ProductNotFoundError(f"Product not found by title: {title}")
        return product_card

    def get_active_card_by_title(self, title: str) -> ProductCardComponent:
        self.found_product(title)
        return self.get_card_by_title(title)

    @step_log.log("Add products to cart: {*args}")
    def add_products_to_cart(self, *args: str) -> None:
        for product_title in args:
            self.add_product_to_cart(product_title)

    @step_log.log("Add product to cart: {product_title}")
    def add_product_to_cart(self, product_title: str) -> None:
        if not self.found_product(product_title):
            raise RuntimeError(
                f"Product with title = [{product_title}] not found in carousel"
            )
        self._locator.add_to_cart(product_title).click()

    # ASSERTIONS
    @step_log.log(
        "Check [{self._component_title}] contains product with title: {product_title}"
    )
    def check_contains_product(self, product_title: str) -> None:
        if not self.found_product(product_title):
            raise AssertionError(
                f"Product with title = [{product_title}] not found in carousel"
            )

    @step_log.log(
        "Check [{self._component_title}] contains expected products: {product_titles}"
    )
    def check_contains_products(self, product_title: str, *product_titles: List[str]):
        not_found_products = self.__carousel_contains_products_titles(
            product_title, *product_titles
        )
        if not_found_products:
            raise AssertionError(
                f"Product carousel expected products not found: {not_found_products}"
            )

    @step_log.log("Check product [{product_title}] has price: {price}")
    def check_product_has_price(self, product_title: str, price) -> None:
        product = self.found_product(product_title)
        if not product:
            raise RuntimeError(
                f"Product with title = [{product_title}] not found in carousel"
            )

        actual_price = product.get_product_price()
        if price != actual_price:
            raise AssertionError(
                f"Product should have price: {price}. Actual: {actual_price}"
            )

    def found_product(self, product_title: str) -> Optional[ProductCardComponent]:

        product_exists = self.__scroll_to_product_card(product_title)
        if not product_exists:
            return None

        product_element = self._locator.active_products().find_element_by_child(
            child="p",
            condition=have.text(product_title),
            element_title=f"Carousel product '{product_title}'",
        )
        return ProductCardComponent(product_element.locator, product_title)

    def __scroll_to_product_card(self, product_title: str) -> bool:
        """Scrolling product carousel slide to slide with expected product title
        Returns:
            True - product exists
            False - product not found
        """
        start_product_title = ""
        while True:

            product_titles = [
                product_card.get_product_title()
                for product_card in self._locator.carousel_products()
                if product_card.get_product_title() != ""
            ]

            # Stop scrolling and return True if product found by title
            if product_title in product_titles:
                return True

            # Stop scrolling and return False if elements repeated
            if start_product_title in product_titles:
                return False

            start_product_title = (
                product_titles[0].title()
                if not start_product_title
                else start_product_title
            )

            self._locator.next().click()
            time.sleep(_CAROUSEL_SCROLL_TIMEOUT)

    def __carousel_contains_products_titles(
        self,
        product_title: str,
        *product_titles: str,
    ) -> list[str]:

        start_product_title = None
        not_found_product_titles = [product_title, *product_titles]

        while True:

            actual_product_titles = [
                product_card.get_product_title()
                for product_card in self._locator.active_products().extract(
                    selector_to_extract_component_title=".productinfo p"
                )
            ]

            # Stop scrolling if all products found or elements repeated
            if (
                not not_found_product_titles
                or start_product_title in actual_product_titles
            ):
                return not_found_product_titles

            start_product_title = (
                product_titles[0].title()
                if not start_product_title
                else start_product_title
            )

            for actual_product_title in actual_product_titles:
                if actual_product_title in not_found_product_titles:
                    not_found_product_titles.remove(actual_product_title)

            if not_found_product_titles:
                self._locator.next().click()

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

    def carousel_slides(self) -> ElementsCollection[UiElement]:
        return ElementsCollection[UiElement](
            self.__root.all(".item"),
            "Carousel Slides",
            UiElement,
        )

    def carousel_products(self) -> ElementsCollection[ProductCardComponent]:
        return ElementsCollection[ProductCardComponent](
            self.__root.all(".item .product-image-wrapper"),
            "Carousel Products",
            ProductCardComponent,
        )

    def active_products(self) -> ElementsCollection[ProductCardComponent]:
        return ElementsCollection[ProductCardComponent](
            self.__root.all(".item.active .product-image-wrapper"),
            "Carousel Products",
            ProductCardComponent,
        )

    def carousel_product(self, product_title: str) -> Optional[ProductCardComponent]:
        return self.carousel_products().find_element_by_child(
            child="p",
            condition=have.text(product_title),
            element_title=f"Carousel product '{product_title}'",
        )

    def active_carousel_product(self, product_title: str) -> UiElement:
        return self.active_carousel_slide().element(
            css_or_xpath_or_by=_PRODUCT_CONTAINER_SELECTOR.format(product_title),
            element_title=f"Product '{product_title}' in active carousel",
        )

    def add_to_cart(self, product_title: str) -> Button:
        return Button(
            self.__root.element(
                f"//div[contains(@class,'productinfo') and ./p[text()='{product_title}']]"
            ).element(".add-to-cart"),
            f"'{product_title}' Add To Cart",
        )

    def previous(self) -> Button:
        return Button(self.__root.element("a[data-slide=prev]"), "Previous slide")

    def next(self) -> Button:
        return Button(self.__root.element("a[data-slide=next]"), "Next slide")
