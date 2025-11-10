import os
import time
from abc import ABC, abstractmethod
from typing import TypeVar, Type

from PIL import Image
from selene import Element, command, browser, be
from selene.support.conditions import not_
from selene.support.conditions.be import visible

from src.util.image_util import crop_image, create_new_image
from src.util.screen_diff import ScreenDiffResult
from src.util.step_logger import step_log
from src.util.system_util import get_path_in_resources

TBaseComponent = TypeVar("TBaseComponent", bound="BaseComponent")


def create_instance_of_base_component(cls: Type[TBaseComponent], element: Element, element_title: str) -> TBaseComponent:
    if not issubclass(cls, BaseComponent):
        raise TypeError(f"Class {cls.__name__} must be a subclass of {BaseComponent.__name__}")
    try:
        return cls(element, element_title)
    except Exception as e:
        raise RuntimeError(f"Failed to create instance of {cls.__name__}: {str(e)}")


class BaseComponent(ABC):

    def __init__(self, root: Element, component_title: str = None):
        self._root = root
        self._component_title = self.__get_component_title(component_title)

    # ACTIONS
    def scroll_to_component(self) -> None:
        self._root.perform(command.js.scroll_into_view)

    def _scroll_to_element(self, element: Element) -> None:
        element.perform(command.js.scroll_into_view)

    # ASSERTIONS
    @step_log.log("Check [{self._component_title}] is visible")
    def check_component_is_visible(self) -> None:
        self._root.should(be.visible)

    @step_log.log("Check [{self._component_title}] is not visible")
    def check_component_is_not_exists(self) -> None:
        self._root.should(not_.existing)

    def _wait_until_stop_scrolling(self) -> None:
        pass

    @abstractmethod
    def check_visible_component_elements(self) -> None:
        pass

    @abstractmethod
    def check_not_visible_component_elements(self) -> None:
        pass

    @step_log.log("Check [{self._component_title}] has expected screenshot: {path_to_screenshot}")
    def check_component_has_screenshot(
        self,
        path_to_screenshot: str,
        percent_of_tolerance: float = 0,
        rewrite_screenshot: bool = False,
        timeout: int = 0,
    ) -> None:
        self._check_element_have_screenshot(
            self._root,
            path_to_screenshot,
            percent_of_tolerance,
            rewrite_screenshot,
            timeout,
        )

    def _check_element_have_screenshot(
        self,
        element: Element,
        path_to_screenshot: str,
        percent_of_tolerance: float = 0,
        rewrite_screenshot: bool = False,
        timeout: int = 0,
    ) -> None:
        """
        Checks if expected and actual screenshots is the same in .
        :param element: element
        :param path_to_screenshot: (str) path to screenshot from resources. Example, "files/img/screenshot/main_page.png"
        """
        abs_path_to_screenshot = get_path_in_resources(path_to_screenshot)
        is_expected_screenshot_not_exists = not os.path.exists(abs_path_to_screenshot)

        element.wait_until(visible)
        self._scroll_to_element(element)

        if timeout > 0:
            time.sleep(timeout)

        actual_screenshot = crop_image(
            byte_image=browser.driver.get_screenshot_as_png(),
            location=element().location,
            size=element().size,
        )

        if is_expected_screenshot_not_exists:
            create_new_image(abs_path_to_screenshot, actual_screenshot)

        expected_screenshot = Image.open(abs_path_to_screenshot, formats=["PNG"])

        ScreenDiffResult(
            expected=expected_screenshot,
            actual=actual_screenshot,
            percent_of_tolerance=percent_of_tolerance,
        )

        if is_expected_screenshot_not_exists or rewrite_screenshot:
            actual_screenshot.save(abs_path_to_screenshot, save_all=True)

    def __get_component_title(self, actual_component_title: str) -> str:
        if actual_component_title:
            return actual_component_title
        else:
            return type(self).__name__

    def _change_component_title(self, new_component_title: str) -> None:
        self._component_title = new_component_title


# class ComponentsCollection(BaseComponent, ABC):
#
#     def __init__(self, root: Element, child_locator: str, collection_title: str, cls: Type[TBaseComponent]):
#         super().__init__(root, collection_title)
#         self._cls = cls
#         self._child_locator = child_locator
#         self._components_collection = None
#
#     def __get_collection(self, cls: Type[TBaseComponent], child_locator: str) -> TBaseComponent:
#         web_elements = self._root.all(child_locator)
#         components_collection = list()
#         for web_element in web_elements:
#             components_collection.append(
#                 create_instance_of_base_component(
#                     cls,
#                     self._root.all(child_locator).el,
#                     None,
#                 )
#             )
#
#     def change_collection_title(self, title: str) -> None:
#         self._collection_title = title
