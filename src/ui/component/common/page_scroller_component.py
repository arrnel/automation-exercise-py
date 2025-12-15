import allure
from selene import Element, be, browser, command
from selene.core.wait import Command
from selene.support.conditions.be import not_

from src.ui.component.base_component import BaseComponent


class PageScrollerComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)

    # ACTIONS
    def scroll_to_top(self) -> None:
        with allure.step("Scroll page to the top"):
            self._root.click()
            self.__wait_until_stop_scrolling()

    # ASSERTIONS
    def check_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are visible"):
            self._root.should(be.visible)

    def check_not_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are not exists"):
            self._root.should(not_.existing)

    def __wait_until_stop_scrolling(self) -> None:
        def func(element: Element):
            element.execute_script(
                """
                    () => {
                        return new Promise((resolve) => {
                            let timeout = 150;
                            let lastScrollPos = window.scrollY;
                            let stableCount = 0;
                            const checkScroll = () => {
                                const currentScrollPos = window.scrollY;
                                if (currentScrollPos === lastScrollPos) {
                                    stableCount++;
                                    if (stableCount >= 3) resolve(true);
                                } else {
                                    stableCount = 0;
                                    lastScrollPos = currentScrollPos;
                                }
                                setTimeout(checkScroll, timeout);
                            };
                            checkScroll();
                        });
                    }
                """,
            )

        wait_until_stop_scrolling_command = Command("wait until stop scrolling", func)
        self._root.perform(wait_until_stop_scrolling_command)
