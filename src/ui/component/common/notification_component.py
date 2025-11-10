import allure
from selene import Element, have, be
from selene.support.conditions import not_

from src.ui.component.base_component import BaseComponent

_SUCCESS_ADD_PRODUCT_TO_CART_MESSAGE = "Your product has been added to cart."
_NOT_AUTHORIZED_MESSAGE = "Register / Login account to proceed on checkout."


class NotificationComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self.__locator = _NotificationComponentLocator(root)

    # ACTIONS
    def close(self) -> None:
        with allure.step("Close notification"):
            self.__locator.close().click()

    def click_on_link(self) -> None:
        with allure.step("Close notification"):
            self.__locator.description_link().click()

    # ASSERTIONS
    def check_notification_has_title(self, text: str) -> None:
        with allure.step(f"Check notification has title: {text}"):
            self.__locator.title().should(have.text(text))

    def check_notification_has_description(self, text: str) -> None:
        with allure.step(f"Check notification has description: {text}"):
            self.__locator.description().should(have.text(text))

    def check_notification_has_success_added_product_message(self) -> None:
        with allure.step("Check notification has success added product to cart message"):
            self.__locator.description().should(have.text(_SUCCESS_ADD_PRODUCT_TO_CART_MESSAGE))

    def check_notification_has_not_authorized_message(self) -> None:
        with allure.step("Check notification has not authorized message"):
            self.__locator.description().should(have.text(_NOT_AUTHORIZED_MESSAGE))

    def check_notification_has_description_link(self, text: str) -> None:
        with allure.step(f"Check notification has description: {text}"):
            self.__locator.description().should(have.attribute("href", text))

    def check_notification_has_success_description_link_text(self, text: str) -> None:
        with allure.step("Check notification has success added product to cart message"):
            self.__locator.description().element("u").should(have.text(text))

    def check_notification_has_screenshot(
        self,
        path_to_screenshot: str,
        percent_of_tolerance: float,
        rewrite_screenshot: bool,
    ) -> None:
        with allure.step("Check notification has screenshot"):
            self._check_element_have_screenshot(
                element=self._root,
                path_to_screenshot=path_to_screenshot,
                percent_of_tolerance=percent_of_tolerance,
                rewrite_screenshot=rewrite_screenshot,
                timeout=0,
            )

    def check_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are visible"):
            self.__locator.title().should(be.visible)
            self.__locator.description().should(be.visible)
            self.__locator.description_link().should(be.visible)
            self.__locator.close().should(be.visible)

    def check_not_visible_component_elements(self) -> None:
        with allure.step(f"Check [{self._component_title}] elements are not exists"):
            self.__locator.title().should(not_.existing)
            self.__locator.description().should(not_.existing)
            self.__locator.description_link().should(not_.existing)
            self.__locator.close().should(not_.existing)


class _NotificationComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def title(self) -> Element:
        return self.__root.element("h4")

    def description(self) -> Element:
        return self.__root.element(".modal-body p:first-child")

    def description_link(self) -> Element:
        return self.__root.element(".modal-body a")

    def close(self) -> Element:
        return self.__root.element(".close-modal")
