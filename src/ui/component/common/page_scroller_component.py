from selene import Element, be, browser
from selene.support.conditions.be import not_

from src.config.config import CFG
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import Button
from src.util.decorator.step_logger import step_log


class PageScrollerComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self.__locator = _PageScrollerComponentLocator(root)

    # ACTIONS
    @step_log.log("Scroll page to the top")
    def scroll_to_top(self) -> None:
        self.__locator.scroll().click()
        self.__wait_until_stop_scrolling()

    # ASSERTIONS
    @step_log.log("Scroll page to the bottom")
    def check_visible_component_elements(self) -> None:
        self._root.should(be.visible)

    def check_not_visible_component_elements(self) -> None:
        self._root.should(not_.existing)

    @step_log.log("Wait stop scrolling")
    def __wait_until_stop_scrolling(self) -> None:
        """
        Wait until scrolling is stopped

        Raises:
            TimeoutError - if scrolling is not stopped before time exceeds CFG.browser_timeout
        """

        script = """
        const timeoutSeconds = arguments[0];
        const done = arguments[arguments.length - 1];

        const maxWaitTime = timeoutSeconds * 1000;
        const startTime = Date.now();

        let previousPosition = window.scrollY || window.pageYOffset;
        let stableTicks = 0;

        const interval = setInterval(() => {
            const currentPosition = window.scrollY || window.pageYOffset;
            const elapsedTime = Date.now() - startTime;

            if (currentPosition === previousPosition) {
                stableTicks++;
            } else {
                stableTicks = 0;
                previousPosition = currentPosition;
            }

            if (stableTicks >= 2) {
                clearInterval(interval);
                done(true);
                return;
            }

            if (elapsedTime >= maxWaitTime) {
                clearInterval(interval);
                done(false);
            }
        }, 100);
        """

        result = browser.driver.execute_async_script(script, CFG.browser_timeout)

        if not result:
            raise TimeoutError(
                f"Scrolling not stopped for {CFG.browser_timeout} seconds"
            )


class _PageScrollerComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def scroll(self) -> Button:
        return Button(self.__root, "Page scroller")
