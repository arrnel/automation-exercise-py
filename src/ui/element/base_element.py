import time
from typing import Optional, override, Union, Tuple, TypeVar, Type, Callable, Iterable

from selene import Element, query, have, be, command
from selene.core.condition import Condition
from selene.core.entity import Collection
from selene.support.conditions.be import existing, visible, not_
from selene.support.conditions.have import text
from selene.support.conditions.not_ import css_class

from src.util.step_logger import step_log, LogLvl

TBaseElement = TypeVar("TBaseElement", bound="BaseElement")


def _create_instance_of_base_element(
    cls: Type[TBaseElement], element: Element, element_title: str
) -> TBaseElement:
    if not issubclass(cls, BaseElement):
        raise TypeError(
            f"Class {cls.__name__} must be a subclass of {BaseElement.__name__}"
        )
    try:
        return cls(element, element_title)
    except Exception as e:
        raise RuntimeError(f"Failed to create instance of {cls.__name__}: {str(e)}")


# ==========================================================
# ELEMENTS
# ==========================================================


class BaseElement:

    def __init__(self, locator: Element, element_title: str):
        self._root = locator
        self._element_title = element_title

    @property
    def element_title(self) -> str:
        return self._element_title

    def change_element_title(self, new_element_title: str) -> None:
        self._element_title = new_element_title

    def get_locator(self) -> Element:
        return self._root

    def get_attribute(self, attribute_name: str) -> str:
        return self._root.get(query.attribute(attribute_name))

    def hover(self, seconds=0) -> None:
        """
        Hovers over the element, triggering its hover state in the browser.

        Args:
            seconds: Duration in seconds to wait after hovering. Default value: 0.
        """
        with step_log.log(
            f"Hover over {self._element_title}{f" for a [{seconds}] second(s)" if seconds > 0 else ""}"
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
        return _create_instance_of_base_element(
            cls, self._root.element(css_or_xpath_or_by), element_title
        )

    def all(
        self,
        css_or_xpath_or_by: Union[str, Tuple[str, str]],
        condition: Condition[Element] = Optional[None],
        collection_title: str = Optional[None],
    ) -> "ElementsCollection":
        return ElementsCollection(
            (
                self._root.all(css_or_xpath_or_by)
                if condition is None
                else self._root.all(css_or_xpath_or_by).by(condition)
            ),
            collection_title or f"{self._element_title} element collection",
        )

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

    def has(self, condition: Condition[Element]) -> bool:
        return self._root.matching(condition)

    def contains(self, condition: Condition[Element]) -> bool:
        return self.has(condition)

    def wait_until(self, condition: Condition[Element]) -> TBaseElement:
        self._root.wait_until(condition)
        return self

    def wait_until_not(self, condition: Condition[Element]) -> None:
        self._root.wait_until(condition.not_)

    def scroll_into_view(self) -> None:
        self._root.perform(command.js.scroll_into_view)


class UiElement(BaseElement):

    def __init__(self, locator: Element, element_title: str):
        super().__init__(locator, element_title)


class Text(BaseElement):

    def __init__(self, locator: Element, element_title: str):
        super().__init__(locator, element_title)

    def get_value(self) -> str:
        return self._root.get(query.value)

    def get_text(self) -> str:
        return self._root.get(query.value)

    @step_log.log("Check [{self._element_title} has text: {value}]")
    def should_have_text(self, value):
        self._root.should(have.exact_text(value))


class Button(BaseElement):

    def __init__(self, locator: Element, element_title: str):
        super().__init__(locator, element_title)

    @step_log.log(
        message="Click on [{self._element_title}] button", log_level=LogLvl.DEBUG
    )
    def click(self) -> None:
        self._root.click()


class Input(BaseElement):

    def __init__(self, locator: Element, element_title: str):
        super().__init__(locator, element_title)

    @step_log.log(
        message="Fill [{self._element_title}]: {value}", log_level=LogLvl.DEBUG
    )
    def set_value(self, value) -> None:
        self._root.set_value(value)

    @step_log.log(
        message="Fill [{self._element_title}]: {value}", log_level=LogLvl.DEBUG
    )
    def type(self, value) -> None:
        self._root.type(value)

    def get_value(self) -> str:
        return self._root.get(query.value)

    def get_text(self) -> str:
        return self._root.get(query.value)

    @step_log.log("Check [{self._element_title} has value: {value}]")
    def should_have_value(self, value):
        self._root.should(have.value(value))


class Select(BaseElement):

    def __init__(
        self, locator: Element, element_title: str, default_value=Optional[None]
    ):
        super().__init__(locator, element_title)
        self.__default_value = default_value

    @step_log.log(
        message="Select [{self._element_title}]: {value}", log_level=LogLvl.DEBUG
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

    def __init__(self, locator: Element, element_title: str):
        super().__init__(locator, element_title)

    @step_log.log(
        message="Set checked [{self._element_title}]: {value}", log_level=LogLvl.DEBUG
    )
    def check(self) -> None:
        self._root.click()

    @step_log.log(
        message="Check [{self._element_title}] value {value} is checked",
        log_level=LogLvl.DEBUG,
    )
    def check_value_is_checked(self) -> None:
        self._root.should(have.value(1))

    @step_log.log(
        message="Check [{self._element_title}] value {value} is unchecked",
        log_level=LogLvl.DEBUG,
    )
    def check_value_is_unchecked(self) -> None:
        self._root.should(have.value(0))


class Panel(BaseElement):
    """Element of AccordionFilter"""

    def __init__(self, locator: Element, element_title: str):
        super().__init__(locator, element_title)

    def select_category(self, category: str) -> None:
        self._root.all("li a").element_by(text(category))

    def __is_expanded(self) -> bool:
        return self._root.element(".panel-collapse").matching(css_class("in"))

    def expand(self) -> "Panel":
        if not self.__is_expanded():
            with step_log.log(f"Expand {self._element_title}"):
                self._root.click()
        return self

    def collapse(self) -> "Panel":
        if self.__is_expanded():
            with step_log.log(f"Collapse {self._element_title}"):
                self._root.click()
        return self

    def should_contains_categories(
        self, *categories: Union[str, Iterable[str]]
    ) -> None:
        self._root.all("li a").should(have.texts(*categories))


class CategoryStat(BaseElement):
    """Element of CategoryStatFilter"""

    def __init__(self, locator: Element, element_title: str):
        super().__init__(locator, element_title)

    @step_log.log("Click on [{self._element_title}]")
    def click(self) -> None:
        self._root.element("a").click()

    @step_log.log("Check [{self._element_title}] has count: {count}")
    def should_have_count(self, count: int) -> None:
        self._root.element(".pull-right").should(have.text(f"({count})"))


# ==========================================================
# COLLECTIONS
# ==========================================================
class ElementsCollection:

    def __init__(
        self,
        collection: Collection,
        collection_title: str,
        cls: Type[TBaseElement] = UiElement,
    ):
        self._collection = collection
        self._collection_title = collection_title
        self._cls = cls

    def change_collection_title(self, title: str) -> None:
        self._collection_title = title

    def size(self) -> int:
        return len(self._collection)

    def filter(self, condition: Condition[Element]) -> Collection:
        return self._collection.by(condition)

    def find_element(
        self,
        condition: Union[Condition[Element], Callable[[Element], None]],
        element_title: str,
    ) -> TBaseElement:
        return _create_instance_of_base_element(
            cls=self._cls,
            element=self._collection.element_by(condition),
            element_title=element_title,
        )

    def filter_by_child(
        self,
        child_locator: str,
        condition: Condition[Element],
        collection_title: str = Optional[None],
    ) -> "ElementsCollection":
        self._collection_title = (
            collection_title
            if collection_title is not None
            else f"{self._collection_title} filtered by: {condition}"
        )
        filtered = self._collection.by(
            lambda parent: condition(parent.element(child_locator))
        )
        return ElementsCollection(filtered, self._collection_title)

    def find_element_by_child(
        self,
        child_locator: str,
        element_title: str,
        condition: Condition[Element] = Optional[None],
        cls: Type[TBaseElement] = Optional[None],
    ) -> TBaseElement:
        return _create_instance_of_base_element(
            cls=cls or self._cls,
            element=self._collection.element_by(
                lambda parent: condition(parent.element(child_locator))
            ),
            element_title=element_title,
        )

    @step_log.log(
        message="Check [{self._collection_title}] contains texts: {args}",
        log_level=LogLvl.DEBUG,
    )
    def should_contains_texts(self, *args: str) -> None:
        self._collection.all("label").should(have.texts(*args))

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
        super().__init__(collection, collection_title)

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
    def should_contains_texts(self, *args: str) -> None:
        self._collection.all("label").should(have.texts(*args))

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
