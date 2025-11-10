import allure
from selene import Element, be
from selene.support.conditions.be import not_

from src.ui.component.base_component import BaseComponent


class PageScrollerComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)

    # ACTIONS
    def scroll_to_top(self) -> None:
        with allure.step("Scroll page to the top"):
            self._root.click()
            self._wait_until_stop_scrolling()

    # ASSERTIONS
    def check_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are visible"):
            self._root.should(be.visible)

    def check_not_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are not exists"):
            self._root.should(not_.existing)
