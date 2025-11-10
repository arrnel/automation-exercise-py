import allure
from selene import Element, have, be
from selene.core.entity import Collection
from selene.support.conditions import not_

from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Button


class BreadcrumbComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self.__locator = _BreadcrumbComponentLocator(root)

    # ACTIONS
    def home(self) -> None:
        with allure.step(f"Navigate to [Home] page from {self._component_title}"):
            self.__locator.home().click()

    def previous_page(self) -> None:
        with allure.step(f"Navigate to [Previous] page from {self._component_title}"):
            self.__get_previous_breadcrumb_element().click()

    # ASSERTIONS
    def check_active_breadcrumb_title(self, title: str) -> None:
        with allure.step(f"Check if active breadcrumb title is {title}"):
            self.__locator.active_breadcrumb().should(have.text(title))

    def check_previous_breadcrumb_title(self, title: str) -> None:
        with allure.step(f"Check previous breadcrumb title is {title}"):
            self.__get_previous_breadcrumb_element().should(have.text(title))

    def check_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are visible"):
            self.__locator.home().should(be.visible)

    def check_not_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are not exists"):
            self.__locator.home().should(not_.existing)

    def __get_previous_breadcrumb_element(self) -> Element:
        all_breadcrumbs = self.__locator.all()
        previous_breadcrumb_idx = len(all_breadcrumbs) - 1

        if previous_breadcrumb_idx < 0:
            raise ValueError("Can't get to previous page breadcrumb")

        return all_breadcrumbs[previous_breadcrumb_idx]


class _BreadcrumbComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def all(self) -> Collection:
        return self.__root.all("li")

    def home(self) -> Button:
        return Button(self.__root.element(".//a[text()='Home']"), "Home")

    def breadcrumb(self, title: str) -> Button:
        return Button(self.__root.element(f".//li[text()='{title}']"), f"Breadcrumb '{title}'")

    def active_breadcrumb(self) -> Button:
        return Button(self.__root.element(".active"), "active_breadcrumb")
