from selene import Element, by, be, have
from selene.support.conditions import not_

from src.ui.component.base_component import BaseComponent
from src.util.step_logger import step_log


class HeaderComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None) -> None:
        super().__init__(root, component_title)
        self.__locator = _HeaderComponentLocator(root)

    # ACTIONS
    @step_log.log("Navigate to the [Main] page by logo")
    def go_to_main_page_by_logo(self) -> None:
        self.__locator.logo().click()

    @step_log.log("Navigate to the [Main] page")
    def go_to_main_page(self) -> None:
        self.__locator.home().click()

    @step_log.log("Navigate to the [Products] page")
    def go_to_products_page(self) -> None:
        self.__locator.products().click()

    @step_log.log("Navigate to the [Cart] page")
    def go_to_cart_page(self) -> None:
        self.__locator.cart().click()

    @step_log.log("Navigate to the [Login] page")
    def go_to_login_page(self) -> None:
        self.__locator.login().click()

    @step_log.log("Logout")
    def logout(self) -> None:
        self.__locator.logout().click()

    @step_log.log("Delete account")
    def delete_account(self) -> None:
        self.__locator.delete_account().click()

    @step_log.log("Navigate to the [Contact us] page")
    def go_to_contact_us_page(self) -> None:
        self.__locator.contact_us().click()

    def is_user_logged_in(self) -> bool:
        return self.__locator.logged_in().matching(be.visible)

    # ACTIONS
    @step_log.log("Check user is logged in")
    def check_user_is_logged_in(self) -> None:
        self.__locator.logged_in().should(be.visible)

    @step_log.log("Check user is logged in as: {text}")
    def check_user_is_logged_in_as(self, text: str) -> None:
        self.__locator.logged_in_as().should(have.text(text))

    @step_log.log("Check user is not authorized")
    def check_user_is_not_authorized(self) -> None:
        self.__locator.login().should(be.visible)

    @step_log.log("Check [{self._component_title}] elements are visible}")
    def check_visible_component_elements(self) -> None:
        self.__locator.logo().should(be.visible)
        self.__locator.home().should(be.visible)
        self.__locator.products().should(be.visible)

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self.__locator.logo().should(not_.existing)
        self.__locator.home().should(not_.existing)
        self.__locator.products().should(not_.existing)


class _HeaderComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def logo(self) -> Element:
        return self.__root.element(".logo")

    def nav_bar(self) -> Element:
        return self.__root.element(".shop-menu")

    def home(self) -> Element:
        return self.nav_bar().element(by.text("Home"))

    def cart(self) -> Element:
        return self.nav_bar().element(by.text("Cart"))

    def products(self) -> Element:
        return self.nav_bar().element(by.text("Products"))

    def sign_up(self) -> Element:
        return self.nav_bar().element(by.text("Signup / Login"))

    def login(self) -> Element:
        return self.sign_up()

    def logout(self) -> Element:
        return self.nav_bar().element(by.text("Logout"))

    def delete_account(self) -> Element:
        return self.nav_bar().element(by.text("Delete Account"))

    def contact_us(self) -> Element:
        return self.nav_bar().element(by.text("Contact us"))

    def logged_in(self) -> Element:
        return self.nav_bar().element(by.text("Logged in as"))

    def logged_in_as(self) -> Element:
        return self.logged_in().element("b")

    def active(self) -> Element:
        return self.nav_bar().element("a[style*='color: orange']")
