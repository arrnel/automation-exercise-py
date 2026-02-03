from selene import Element, by, be

from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import UiElement, TextLink, Text, Button
from src.util.decorator.step_logger import step_log


class HeaderComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None) -> None:
        super().__init__(root, component_title)
        self.__locator = _HeaderComponentLocator(root)

    # ACTIONS
    @step_log.log("Navigate to the [Main] page by header logo")
    def go_to_main_page_by_logo(self) -> None:
        self.__locator.logo().click()

    @step_log.log("Navigate to the [Main] page by header")
    def go_to_main_page(self) -> None:
        self.__locator.home().click()

    @step_log.log("Navigate to the [Products] page by header")
    def go_to_products_page(self) -> None:
        self.__locator.products().click()

    @step_log.log("Navigate to the [Cart] page by header")
    def go_to_cart_page(self) -> None:
        self.__locator.cart().click()

    @step_log.log("Navigate to the [Login] page by header")
    def go_to_login_page(self) -> None:
        self.__locator.login().click()

    @step_log.log("Logout")
    def logout(self) -> None:
        self.__locator.logout().click()

    @step_log.log("Delete account")
    def delete_account(self) -> None:
        self.__locator.delete_account().click()

    @step_log.log("Navigate to the [Contact us] page by header")
    def go_to_contact_us_page(self) -> None:
        self.__locator.contact_us().click()

    def is_user_logged_in(self) -> bool:
        return self.__locator.logged_in().matching(be.visible)

    # ACTIONS
    @step_log.log("Check user is logged in in header")
    def check_user_is_logged_in(self) -> None:
        self.__locator.logged_in().should_be_visible()

    @step_log.log("Check user is logged in in header as: {text}")
    def check_user_is_logged_in_as(self, text: str) -> None:
        self.__locator.logged_in_as().should_have_text(text)

    @step_log.log("Check user is not authorized")
    def check_user_is_not_authorized(self) -> None:
        self.__locator.login().should_be_visible()

    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self.__locator.logo().should_be_visible()
        self.__locator.home().should_be_visible()
        self.__locator.products().should_be_visible()

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self.__locator.logo().should_not_exists()
        self.__locator.home().should_not_exists()
        self.__locator.products().should_not_exists()


class _HeaderComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def logo(self) -> Button:
        return Button(self.__root.element(".logo"), "Logo")

    def nav_bar(self) -> UiElement:
        return UiElement(self.__root.element(".shop-menu"), "Nav Bar")

    def home(self) -> TextLink:
        return self.nav_bar().element(by.text("Home"), "Home", TextLink)

    def cart(self) -> TextLink:
        return self.nav_bar().element(by.text("Cart"), "Cart", TextLink)

    def products(self) -> TextLink:
        return self.nav_bar().element(by.text("Products"), "Products", TextLink)

    def sign_up(self) -> TextLink:
        return self.nav_bar().element(by.text("Signup / Login"), "Sign Up", TextLink)

    def login(self) -> TextLink:
        return self.nav_bar().element(by.text("Signup / Login"), "Login", TextLink)

    def logout(self) -> TextLink:
        return self.nav_bar().element(by.text("Logout"), "Logout", TextLink)

    def delete_account(self) -> TextLink:
        return self.nav_bar().element(
            by.text("Delete Account"), "Delete Account", TextLink
        )

    def contact_us(self) -> TextLink:
        return self.nav_bar().element(by.text("Contact us"), "Contact Us", TextLink)

    def logged_in(self) -> TextLink:
        return self.nav_bar().element(by.text("Logged in as"), "Logged in", TextLink)

    def logged_in_as(self) -> Text:
        return self.logged_in().element("b", "Logged in as", Text)
