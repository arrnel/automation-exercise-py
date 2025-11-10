from typing import Union, Iterable

from selene import Element, have

from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Input, Button, ElementsCollection, Panel, CategoryStat
from src.util.step_logger import step_log


class SearchFilter(BaseComponent):

    def __init__(self, root: Element, component_name: str):
        super().__init__(root, component_name)
        self.__locator = _SearchFilterLocator(self._root)

    @step_log.log("Search in [{self.__component_name}] by query: {query}")
    def search(self, query: str):
        self.__locator.input().set_value(query)
        self.__locator.submit().click()

    def check_visible_component_elements(self) -> None:
        self.__locator.input().should_be_visible()
        self.__locator.submit().should_be_visible()

    def check_not_visible_component_elements(self) -> None:
        self.__locator.input().should_not_exists()
        self.__locator.submit().should_not_exists()


class AccordionFilter(BaseComponent):

    def __init__(self, locator: Element, component_title: str):
        super().__init__(locator, component_title)
        self.__panels = ElementsCollection(self._root.all(".panel"), f"{component_title} groups", Panel)

    # ACTIONS
    @step_log.log("Filter in {self._component_title} by group = [{group}] and category = [{category}]")
    def select_group_category(self, group: str, category: str) -> None:
        self.__get_panel(group).expand().select_category(category)

    # Assertions
    @step_log.log("Check {self._component_title} group [{group}] contains categories: [{categories}]")
    def should_contains_categories_group_category(self, group: str, *categories: Union[str, Iterable[str]]) -> None:
        self.__get_panel(group).should_contains_categories(*categories)

    def check_visible_component_elements(self) -> None:
        self.__panels.should_have_size_greater_than(0)

    def check_not_visible_component_elements(self) -> None:
        self.__panels.should_have_size(0)

    def __get_panel(self, group: str) -> Panel:
        return self.__panels.find_element_by_child(
            cls=Panel,
            child_locator=".panel-collapse",
            condition=have.attribute("id", group),
            element_title=f"{self._component_title} group {group}",
        )


class CategoryStatFilter(BaseComponent):

    def __init__(self, locator: Element, component_title: str):
        super().__init__(locator, component_title)
        self.__category_stats = ElementsCollection(self._root.all("li"), f"{component_title} category", CategoryStat)

    # ACTIONS
    @step_log.log("Select in group = [{group}] category = [{category}]")
    def select(self, category: str) -> None:
        self.__get_category_stat(category).click(category)

    # Assertions
    @step_log.log("Check {self._component_title} contains category {category} with count: [{count}]")
    def should_have_category_with_count(self, category: str, count: int) -> None:
        self.__get_category_stat(category).should_have_count(count)

    def __get_category_stat(self, title: str) -> CategoryStat:
        return self.__category_stats.find_element_by_child(
            cls=CategoryStat,
            child_locator="li",
            condition=have.text(title),
            element_title=f"{self._component_title} category stat {title}",
        )

    def check_visible_component_elements(self) -> None:
        self.__category_stats.should_have_size_greater_than(0)

    def check_not_visible_component_elements(self) -> None:
        self.__category_stats.should_have_size(0)


class _SearchFilterLocator:

    def __init__(self, root: Element):
        self.__root = root

    def input(self) -> Input:
        return Input(self.__root.element("#search_product"), "Search product")

    def submit(self) -> Button:
        return Button(self.__root.element("submit_search"), "Submit search")
