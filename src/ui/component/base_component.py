from abc import ABC, abstractmethod
from typing import Type

from selene import Element, command, be
from selene.support.conditions import not_

from src.config.config import CFG
from src.ui.element.base_element import UiElement
from src.util.decorator.step_logger import step_log
from src.util.screenshot import screenshot_util
from src.util.type_util import TBaseComponent


class BaseComponent(ABC):

    def __init__(self, root: Element, component_title: str = None):
        self._root = root
        self._component_title = component_title

    @classmethod
    def from_element(cls: Type[TBaseComponent], element: "UiElement") -> TBaseComponent:
        return cls(element.locator, element.element_title)

    # ACTIONS
    @step_log.log("Scroll to [{self._component_title}]")
    def scroll_to_component(self) -> None:
        self._root.perform(command.js.scroll_into_view)

    # ASSERTIONS
    @step_log.log("Check [{self._component_title}] is visible")
    def check_component_is_visible(self) -> None:
        self._root.should(be.visible)

    @step_log.log("Check [{self._component_title}] is not exists")
    def check_component_is_not_exists(self) -> None:
        self._root.should(not_.existing)

    @step_log.log("Check [{self._component_title}] is not visible")
    def check_component_is_not_visible(self) -> None:
        self._root.should(not_.visible)

    @abstractmethod
    def check_visible_component_elements(self) -> None:
        pass

    @abstractmethod
    def check_not_visible_component_elements(self) -> None:
        pass

    @step_log.log(
        "Check [{self._component_title}] has expected screenshot: {path_to_screenshot}"
    )
    def check_component_has_screenshot(
        self,
        path_to_screenshot: str,
        percent_of_tolerance: float = CFG.default_percent_of_tolerance,
        rewrite_screenshot: bool = False,
        hover: bool = False,
        timeout: float = CFG.default_screenshot_timeout,
    ) -> None:

        self._root.should(be.visible)

        actual_screenshot = screenshot_util.take_element_screenshot(
            self._root, hover, timeout
        )
        screenshot_util.compare_and_save_screenshot(
            actual_screenshot=actual_screenshot,
            path_to_screenshot=path_to_screenshot,
            percent_of_tolerance=percent_of_tolerance,
            rewrite_screenshot=rewrite_screenshot,
            component_name=self._component_title,
        )

    @property
    def component_title(self) -> str:
        return self._component_title

    def change_component_title(self, new_component_title: str) -> None:
        self._component_title = new_component_title

    @property
    def locator(self):
        return self._root
