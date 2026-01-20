import logging
import time
from abc import ABC
from pathlib import Path
from typing import (
    Optional,
    override,
    Union,
    Tuple,
    Type,
    Iterable,
    Generic,
    List,
)

import matplotlib
from selene import Element, query, have, be, command, browser, Collection
from selene.core.condition import Condition
from selene.core.wait import Command
from selene.support.conditions.be import existing, visible, not_
from selene.support.conditions.have import text, css_class

from src.config.config import CFG
from src.model.enum.remote_type import RemoteType
from src.service.remote.moon_artifact_service import MoonArtifactApiService
from src.service.remote.selenoid_artifact_service import SelenoidArtifactApiService
from src.util import system_util
from src.util.decorator.step_logger import step_log, LogLvl
from src.util.screenshot import screenshot_util
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore
from src.util.type_util import TBaseElement, TElementOrComponent


# ==========================================================
# ELEMENTS
# ==========================================================
class BaseElement(ABC):

    def __init__(self, root: Element, element_title: str):
        self._root = root
        self._element_title = element_title

    def get_attribute(self, attribute_name: str) -> str:
        return self._root.get(query.attribute(attribute_name))

    def hover(self, seconds=0) -> None:
        """
        Hovers over the element, triggering its hover state in the browser.

        Args:
            seconds: Duration in seconds to wait after hovering. Default value: 0.
        """
        with step_log.log(
            f"Hover over {self._element_title}"
            f"{f" for a [{seconds}] second(s)" if seconds > 0 else ""}"
        ):
            self._root.hover()
            if seconds > 0:
                time.sleep(seconds)

    def element(
        self,
        css_or_xpath_or_by: Union[str, Tuple[str, str]],
        element_title: str,
        cls: Type[TBaseElement] = "UiElement",
    ) -> TBaseElement:
        return cls(self._root.element(css_or_xpath_or_by), element_title)

    def all(
        self,
        css_or_xpath_or_by: Union[str, Tuple[str, str]],
        condition: Condition[Element],
        collection_title: str,
        cls: Type[TElementOrComponent],
    ) -> "ElementsCollection":
        return ElementsCollection(
            (
                self._root.all(css_or_xpath_or_by)
                if condition is None
                else self._root.all(css_or_xpath_or_by).by(condition)
            ),
            collection_title or f"{self._element_title} element collection",
            cls,
        )

    def has(self, condition: Condition[Element]) -> bool:
        return self._root.matching(condition)

    def not_has(self, condition: Condition[Element]) -> bool:
        return self._root.matching(condition.not_)

    @step_log.log(
        message="Check [{self._element_title}] should: {condition}",
        log_level=LogLvl.DEBUG,
    )
    def should(self, condition: Condition[Element]) -> None:
        self._root.should(condition)

    @step_log.log(
        message="Check [{self._element_title}] should be: {condition}",
        log_level=LogLvl.DEBUG,
    )
    def should_be(self, condition: Condition[Element]) -> None:
        self._root.should(condition)

    @step_log.log(
        message="Check [{self._element_title}] should have: {condition}",
        log_level=LogLvl.DEBUG,
    )
    def should_have(self, condition: Condition[Element]) -> None:
        self._root.should(condition)

    @step_log.log(
        message="Check [{self._element_title}] should: {condition}",
        log_level=LogLvl.DEBUG,
    )
    def should_not(self, condition: Condition[Element]) -> None:
        self._root.should(condition.not_)

    @step_log.log(
        message="Check [{self._element_title}] should not be: {condition}",
        log_level=LogLvl.DEBUG,
    )
    def should_not_be(self, condition: Condition[Element]) -> None:
        self._root.should(condition.not_)

    @step_log.log(
        message="Check [{self._element_title}] should not have: {condition}",
        log_level=LogLvl.DEBUG,
    )
    def should_not_have(self, condition: Condition[Element]) -> None:
        self._root.should(condition.not_)

    @step_log.log(
        message="Check [{self._element_title}] is visible", log_level=LogLvl.DEBUG
    )
    def should_be_visible(self):
        self._root.should(be.visible)

    @step_log.log(
        message="Check [{self._element_title}] is not exists", log_level=LogLvl.DEBUG
    )
    def should_not_exists(self):
        self._root.should(not_.existing)

    def is_exists(self):
        return self._root.matching(existing)

    def is_visible(self):
        return self._root.matching(visible)

    def matching(self, condition: Condition[Element]) -> bool:
        return self._root.matching(condition)

    def contains(self, condition: Condition[Element]) -> bool:
        return self.matching(condition)

    def wait_until(self, condition: Condition[Element]) -> TBaseElement:
        self._root.wait_until(condition)
        return self

    def wait_until_not(self, condition: Condition[Element]) -> None:
        self._root.wait_until(condition.not_)

    def scroll_into_view(self) -> None:
        self._root.perform(command.js.scroll_into_view)

    def highlight(self, color: str = "red", border_size: int = 2) -> None:
        """
        Add highlight to element
        :param color: (str) - color of border. Examples: red, green, blue, yellow, ...
        :param border_size: (int) - width of border in px. Should be greater than 0
        """
        try:
            c_hex = matplotlib.colors.cnames[color]
        except Exception as ex:
            logging.warn(f"Invalid color value: {color}. Exception: {ex}")

        if border_size < 0:
            logging.warn(
                f"Invalid border size: {border_size}. Should be greater than 0"
            )

        def func(element: Element):
            element.execute_script(
                """
                element.style.border = arguments[0];
                return null;
                """,
                f"{border_size}px solid {c_hex}",
            )

        highlight_command = Command("highlight element", func)
        self._root.perform(highlight_command)

    @step_log.log("Check [{self._element_title}] element has screenshot")
    def check_element_has_screenshot(
        self,
        path_to_screenshot: str,
        percent_of_tolerance: float = CFG.default_percent_of_tolerance,
        rewrite_screenshot: bool = False,
        hover: bool = False,
        timeout: float = 0,
    ) -> None:
        """
        Checks if the element screenshot matches the expected screenshot.
        """
        self._root.should(be.visible)

        actual_screenshot = screenshot_util.take_element_screenshot(
            self._root, hover, timeout
        )
        screenshot_util.compare_and_save_screenshot(
            actual_screenshot=actual_screenshot,
            path_to_screenshot=path_to_screenshot,
            percent_of_tolerance=percent_of_tolerance,
            rewrite_screenshot=rewrite_screenshot,
            component_name=self.element_title,
        )

    @property
    def element_title(self) -> str:
        return self._element_title

    def change_element_title(self, new_element_title: str) -> None:
        self._element_title = new_element_title

    @property
    def locator(self) -> Element:
        return self._root


class UiElement(BaseElement):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)


class Text(BaseElement):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)

    def get_text(self) -> str:
        return self._root.get(query.text)

    @step_log.log("Check [{self._element_title} has text: {value}]")
    def should_have_text(self, value):
        self._root.should(have.exact_text(value))


class Link(BaseElement):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)

    @step_log.log("Click on [{self._element_title}]")
    def click(self) -> None:
        self._root.click()

    def navigate(self) -> None:
        link = self._root.get(query.attribute("href"))
        with step_log.log(f"Navigate by {self._element_title} link: {link}"):
            browser.open(link)

    @step_log.log("Check [{self._element_title} has link: {value}]")
    def should_have_link(self, link):
        self._root.should(have.attribute("href", link))


class TextLink(Text, Link):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)


class Button(BaseElement):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)

    @step_log.log(
        message="Click on [{self._element_title}] button",
        log_level=LogLvl.DEBUG,
    )
    def click(self, by_js: bool = False) -> None:

        if not by_js:
            self._root.click()
            return

        self._root.perform(command.js.click)


class DownloadableButton(Button):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)

    def download(
        self,
        file_name: str,
        by_js: bool = False,
        retries: int = 5,
        delay: float = 1.0,
    ) -> str:
        """
        Download file. If test runs in remote env, copy file from browser container into test container.
        Args:
            file_name (str): Name of file to download.
            by_js (bool): If true, click on button by js.
            retries (int): Number of times to retry.
            delay (float): Delay between retries.
        Returns:
            str: Path to downloaded file.
        """

        self.click(by_js=by_js)
        test_title = ThreadSafeTestThreadsStore().current_thread_test_name()
        test_dir = f"{CFG.browser_download_dir}/{test_title}"
        abs_file_path = f"{test_dir}/{file_name}"

        if CFG.is_local():
            browser.wait_until(
                lambda _: Path(abs_file_path).is_file(),
            )
            return abs_file_path

        override_test_dir = f"{CFG.browser_override_downloaded_file_dir}/{test_title}"
        override_abs_file_path = f"{override_test_dir}/{file_name}"
        remote_service = (
            SelenoidArtifactApiService()
            if CFG.remote_type == RemoteType.SELENOID
            else MoonArtifactApiService()
        )
        container_id = remote_service.get_container_id(browser.driver.session_id)
        browser.wait_until(
            lambda _: system_util.file_exists_in_docker_container(
                container_id, abs_file_path
            )
        )
        content = remote_service.get_file(
            browser.driver.session_id, file_name, retries=retries, delay=delay
        )
        system_util.create_folder(override_test_dir)
        system_util.save_as_file(override_abs_file_path, content)
        return override_abs_file_path


class Input(BaseElement):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)

    @step_log.log(
        message="Fill [{self._element_title}]: {value}",
        log_level=LogLvl.DEBUG,
    )
    def set_value(self, value) -> None:
        self._root.set_value(value)

    @step_log.log(
        message="Fill [{self._element_title}]: {value}",
        log_level=LogLvl.DEBUG,
    )
    def type(self, value) -> None:
        self._root.type(value)

    def get_value(self) -> str:
        return self._root.get(query.value)

    def get_text(self) -> str:
        return self._root.get(query.text)

    @step_log.log("Check [{self._element_title} has value: {value}]")
    def should_have_value(self, value):
        self._root.should(have.value(value))


class Select(BaseElement):

    def __init__(self, root: Element, element_title: str, default_value=Optional[None]):
        super().__init__(root, element_title)
        self.__default_value = default_value

    @step_log.log(
        message="Select [{self._element_title}]: {value}",
        log_level=LogLvl.DEBUG,
    )
    def select(self, value: Union[str | int], submit_by_click: bool = False) -> None:
        self._root.perform(command.js.scroll_into_view)
        self._root.click()
        self._root.type(value)
        if submit_by_click:
            self._root.element(
                f"option[value='{value}']"
            ).click()  # Sometimes Selene could not select option only by typing

    def select_default(self) -> None:
        if self.__default_value is not None:
            self.select(self.__default_value)
        else:
            raise RuntimeError(f"Select [{self._element_title}] has not default value")

    @step_log.log(
        message="Check [{self._element_title}] contains values: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_contains_values(self, *args) -> None:
        self._root.all("option").should(have.texts(*args))

    @step_log.log(
        message="Check [{self._element_title}] not contains values: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_not_contains_values(self, *args: str) -> None:
        self._root.all("option").should(have.texts(*args).not_)

    @step_log.log(
        message="Check [{self._element_title}] contains values in same order: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_contains_values_in_same_order(self, *args: str) -> None:
        self._root.all("option").should(have.exact_texts(*args))

    @step_log.log(
        message="Check [{self._element_title}] has values: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_values(self, *args: str) -> None:
        self._root.all("option").should(have.values(*args))

    @step_log.log(
        message="Check [{self._element_title}] has values in same order: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_values_in_same_order(self, *args: str) -> None:
        self._root.all("option").should(have.values(*args))


class Checkbox(BaseElement):

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)

    @step_log.log(
        message="Set checked [{self._element_title}]",
        log_level=LogLvl.DEBUG,
    )
    def check(self) -> None:
        self._root.click()

    @step_log.log(
        message="Check [{self._element_title}] is checked",
        log_level=LogLvl.DEBUG,
    )
    def check_value_is_checked(self) -> None:
        self._root.should(have.value(1))

    @step_log.log(
        message="Check [{self._element_title}] is unchecked",
        log_level=LogLvl.DEBUG,
    )
    def check_value_is_unchecked(self) -> None:
        self._root.should(have.value(0))


class Panel(BaseElement):
    """Element of AccordionFilter"""

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)
        self.__locator = _PanelLocator(root, element_title)

    def select_category(self, category: str) -> None:
        self.__locator.categories().element_by(text(category.upper())).click()

    def __is_expanded(self) -> bool:
        return self.__locator.panel_content_wrapper().matching(css_class("in"))

    def expand(self) -> "Panel":
        expanded = self.__is_expanded()
        if not expanded:
            with step_log.log(f"Expand {self._element_title}"):
                self.__locator.expander().click()
        return self

    def collapse(self) -> "Panel":
        if self.__is_expanded():
            with step_log.log(f"Collapse {self._element_title}"):
                self.__locator.expander().click()
        return self

    def should_contains_categories(
        self, *categories: Union[str, Iterable[str]]
    ) -> None:
        self._root.all("li a").should(have.texts(*categories))


class _PanelLocator:

    def __init__(self, root: Element, element_title: str):
        self.__root = root
        self.__element_title = element_title

    def categories(self) -> Collection:
        return self.__root.all("li a")

    def expander(self) -> Button:
        return Button(
            self.__root.element(".pull-right"), self.__element_title + " expander"
        )

    def panel_content_wrapper(self):
        return UiElement(
            self.__root.element(".panel-collapse"),
            self.__element_title + " categories wrapper",
        )


class CategoryStat(BaseElement):
    """Element of CategoryStatFilter"""

    def __init__(self, root: Element, element_title: str):
        super().__init__(root, element_title)

    @step_log.log("Click on [{self._element_title}]")
    def click(self) -> None:
        self._root.element("a").click()

    @step_log.log("Check [{self._element_title}] has count: {count}")
    def should_have_count(self, count: int) -> None:
        self._root.element(".pull-right").should(have.text(f"({count})"))


# ==========================================================
# COLLECTIONS
# ==========================================================
class ElementsCollection(Generic[TElementOrComponent], Iterable[TElementOrComponent]):

    def __init__(
        self,
        collection: Collection,
        collection_title: str,
        cls: Type[TElementOrComponent],
    ):
        self._collection = collection
        self._collection_title = collection_title
        self._cls = cls

    def __iter__(self):
        for el in self._collection:
            yield self._cls(el, self._collection_title)

    def __len__(self):
        return len(self._collection)

    def filter(
        self, condition: Condition[Element], collection_title: str
    ) -> "ElementsCollection[TElementOrComponent]":
        return ElementsCollection(
            self._collection.by(condition),
            collection_title,
            self._cls,
        )

    def filter_by_child(
        self,
        child: Union[str, Tuple[str, str]],
        condition: Condition[Element],
        collection_title: str,
    ) -> "ElementsCollection[TElementOrComponent]":

        filtered = self._collection.by(lambda el: el.element(child).matching(condition))

        return ElementsCollection(
            filtered,
            collection_title or f"{self._collection} filtered by child [{child}]",
            self._cls,
        )

    def find_element(
        self, condition: Condition[Element], cls
    ) -> Optional[TElementOrComponent]:
        el = self._collection.element_by(condition)
        return cls(el, self._collection_title)

    def find_element_by_child(
        self,
        child: Union[str, Tuple[str, str]],
        condition: Condition[Element],
        element_title: str,
    ) -> Optional[TElementOrComponent]:
        for _, parent in enumerate(self._collection):
            el = parent.element(child)
            if el.matching(condition):
                return self._cls(parent, element_title)
        return None

    def extract(
        self,
        selector_to_extract_component_title: Optional[
            Union[str, Tuple[str, str]]
        ] = None,
    ) -> List[TElementOrComponent]:
        return [
            self._cls(
                el,
                (
                    ""
                    if selector_to_extract_component_title is None
                    else el.element(selector_to_extract_component_title).get(query.text)
                ),
            )
            for el in self._collection
        ]

    def extract_as(
        self,
        cls,
        selector_to_extract_component_title: Optional[
            Union[str, Tuple[str, str]]
        ] = None,
    ):
        return [
            cls(
                el,
                (
                    ""
                    if selector_to_extract_component_title is None
                    else el.element(selector_to_extract_component_title).get(query.text)
                ),
            )
            for el in self._collection
        ]

    @step_log.log(
        message="Check [{self._collection_title}] contains texts: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_contains_texts(self, text: str, *texts: str) -> None:
        """
        Assert if collection contains elements with expected texts.

        Example: Success result:
            expected_values: ["Apple", "Kiwi"]
            actual_values: ["Peach", "Apple", "Lemon", "Kiwi", "Orange"]
            Status: pass

        Failed result:
            expected_values: ["Orange"]
            actual_values: ["Peach", "Apple"]
            Status: failed

        Raises:
             AssertionError: with not found expected texts.
        """
        all_expected_texts = {text, *texts}
        all_actual_texts = {element.get(query.text) for element in self._collection}
        mismatched_values = all_expected_texts - all_actual_texts
        if mismatched_values:
            raise AssertionError(f"Not found expected values: {mismatched_values}")

    @step_log.log(
        message="Check [{self._collection_title}] contains texts in the same order: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_contains_texts_in_same_order(self, *args: str) -> None:
        self._collection.all("label").should(have.texts(*args))

    @step_log.log(
        message="Check [{self._collection_title}] has texts: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_texts(self, *args: str) -> None:
        self._collection.should(have.exact_texts(*args))

    @step_log.log(
        message="Check [{self._collection_title}] has texts in same order: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_texts_in_same_order(self, *args: str) -> None:
        self._collection.should(have.exact_texts(*args))

    @step_log.log(
        message="Check [{self._collection_title}] has size: {number}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_size(self, number: int):
        self._collection.should(have.size(number))

    @step_log.log(
        message="Check [{self._collection_title}] has size greater than: {number}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_size_greater_than(self, number: int):
        self._collection.should(have.size_greater_than(number))

    @step_log.log(
        message="Check [{self._collection_title}] has size less than: {number}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_size_less_than(self, number: int):
        self._collection.should(have.size_less_than(number))


class RadioButtons(ElementsCollection):

    def __init__(self, collection: Collection, collection_title: str):
        super().__init__(collection, collection_title, UiElement)

    @step_log.log(
        "Pick {self._collection_title} value: {value}", log_level=LogLvl.DEBUG
    )
    def pick(self, value: str) -> None:
        self._collection.all("input[type=radio]").element_by(have.value(value)).click()

    @step_log.log(
        "Check {self._collection_title} value is picked: {value}",
        log_level=LogLvl.DEBUG,
    )
    def should_be_picked(self, value: str) -> None:
        self._collection.all("input[type=radio]").element_by(have.value(value)).should(
            be.selected
        )

    @override
    @step_log.log(
        "Check {self._collection_title} contains values: {args}", log_level=LogLvl.DEBUG
    )
    def should_contains_texts(self, *texts: str) -> None:
        self._collection.all("label").should(have.texts(*texts))

    @override
    @step_log.log(
        "Check {self._collection_title} contains values in same order: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_contains_texts_in_same_order(self, *args: str) -> None:
        self._collection.all("label").should(have.texts(*args))

    @override
    @step_log.log(
        "Check {self._collection_title} has values: {args}", log_level=LogLvl.DEBUG
    )
    def should_have_texts(self, *args: str) -> None:
        self._collection.all("label").should(have.exact_texts(*args))

    @override
    @step_log.log(
        "Check {self._collection_title} has values in same order: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_have_texts_in_same_order(self, *args: str) -> None:
        self._collection.all("label").should(have.exact_texts(*args))
