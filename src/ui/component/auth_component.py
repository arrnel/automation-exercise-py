from selene import Element, be, have
from selene.support.conditions import not_
from selene.support.conditions.be import existing

from src.model.enum.user_title import UserTitle
from src.model.user import User
from src.ui.component.base_component import BaseComponent
from src.ui.element.base_element import (
    Input,
    Checkbox,
    Select,
    Button,
    Text,
    RadioButtons,
    UiElement,
)
from src.util.decorator.step_logger import step_log


class LoginComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self.__locator = _LoginComponentLocator(self._root)

    # ACTIONS
    @step_log.log("Sign in by email and password")
    def login(self, email: str, password: str) -> None:
        self.__fill_email(email)
        self.__fill_password(password)
        self.__submit()

    def __fill_email(self, email: str) -> None:
        self.__locator.email().set_value(email)

    def __fill_password(self, password: str) -> None:
        self.__locator.password().set_value(password)

    def __submit(self) -> None:
        self.__locator.submit().click()

    # ASSERTIONS
    def check_login_error_has_message(self, text: str) -> None:
        self.__locator.error().should(have.exact_text(text))

    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self.__locator.email().should(be.visible)
        self.__locator.password().should(be.visible)
        self.__locator.submit().should(be.visible)

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self.__locator.email().should(not_.existing)
        self.__locator.password().should(not_.existing)
        self.__locator.submit().should(not_.existing)


class LoginSignUpComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self.__locator = _LoginSignUpComponentLocator(self._root)

    @step_log.log("Pre sign up")
    def sign_up(self, name: str, email: str):
        self.__fill_data(name, email)
        self.__submit()

    @step_log.log("Fill pre sign up data")
    def __fill_data(self, name: str, email: str) -> None:
        self.__fill_name(name)
        self.__fill_email(email)

    def __fill_name(self, name: str):
        self.__locator.name().set_value(name)

    def __fill_email(self, email: str):
        self.__locator.email().set_value(email)

    def __submit(self):
        self.__locator.submit().click()

    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self.__locator.email().should(be.visible)
        self.__locator.name().should(be.visible)
        self.__locator.submit().should(be.visible)

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self.__locator.email().should(not_.existing)
        self.__locator.name().should(not_.existing)
        self.__locator.submit().should(not_.existing)


class SignUpComponent(BaseComponent):

    def __init__(self, root: Element, component_title: str = None):
        super().__init__(root, component_title)
        self.__locator = _SignUpComponentLocator(self._root)

    # ACTIONS
    @step_log.log("Send sign up user data")
    def send_user_data(self, user: User):
        self.__fill_user_data(user)
        self.__submit()

    @step_log.log("Fill user data")
    def __fill_user_data(self, user: User):
        self.__pick_user_title(user.user_title)
        self.__fill_name(user.name)
        self.__fill_password(user.password)
        self.__select_birth_day(user.birth_day)
        self.__select_birth_month(user.birth_month)
        self.__select_birth_year(user.birth_year)
        self.__select_newsletter()
        self.__select_special_offers()
        self.__fill_first_name(user.first_name)
        self.__fill_last_name(user.last_name)
        self.__fill_company(user.company)
        self.__fill_address1(user.address1)
        self.__fill_address2(user.address2)
        self.__select_country(user.country)
        self.__fill_state(user.state)
        self.__fill_city(user.city)
        self.__fill_zip_code(user.zip_code)
        self.__fill_mobile_phone(user.phone_number)

    def __pick_user_title(self, user_title: UserTitle) -> None:
        self.__locator.user_titles().pick(user_title.value)

    def __fill_name(self, name: str) -> None:
        self.__locator.name().set_value(name)

    def __fill_password(self, password: str) -> None:
        self.__locator.password().set_value(password)

    def __select_birth_day(self, birth_day: int) -> None:
        self.__locator.birth_day().select(birth_day)

    def __select_birth_month(self, birth_month: int) -> None:
        self.__locator.birth_month().select(birth_month)

    def __select_birth_year(self, birth_year: int) -> None:
        self.__locator.birth_year().select(birth_year)

    def __select_newsletter(self) -> None:
        self.__locator.newsletter().check()

    def __select_special_offers(self) -> None:
        self.__locator.special_offers().check()

    def __fill_first_name(self, first_name: str) -> None:
        self.__locator.first_name().set_value(first_name)

    def __fill_last_name(self, last_name: str) -> None:
        self.__locator.last_name().set_value(last_name)

    def __fill_company(self, company: str) -> None:
        self.__locator.company().set_value(company)

    def __fill_address1(self, address1: str) -> None:
        self.__locator.address1().set_value(address1)

    def __fill_address2(self, address2: str) -> None:
        self.__locator.address2().set_value(address2)

    def __select_country(self, country: str) -> None:
        self.__locator.country().select(country, True)

    def __fill_state(self, state: str) -> None:
        self.__locator.state().set_value(state)

    def __fill_city(self, city: str) -> None:
        self.__locator.city().set_value(city)

    def __fill_zip_code(self, zip_code: str) -> None:
        self.__locator.zip_code().set_value(zip_code)

    def __fill_mobile_phone(self, mobile_phone: str) -> None:
        self.__locator.mobile_number().set_value(mobile_phone)

    def __submit(self) -> None:
        self.__locator.submit().click()

    # ASSERTIONS
    @step_log.log("Check [{self._component_title}] elements are visible")
    def check_visible_component_elements(self) -> None:
        self.__locator.user_titles_wrapper().should_be_visible()
        self.__locator.birth_day().should_be_visible()
        self.__locator.company().should_be_visible()
        self.__locator.country().should_be_visible()

    @step_log.log("Check [{self._component_title}] elements are not exists")
    def check_not_visible_component_elements(self) -> None:
        self.__locator.user_titles_wrapper().should_not_be(existing)
        self.__locator.birth_day().should_not_exists()
        self.__locator.company().should_not_exists()
        self.__locator.country().should_not_exists()


class _LoginComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def email(self):
        return Input(self.__root.element("[data-qa=login-email]"), "Email")

    def password(self):
        return Input(self.__root.element("[data-qa=login-password]"), "Password")

    def submit(self):
        return Button(self.__root.element("[data-qa=login-button]"), "Login")

    def error(self):
        return Text(self.__root.element("p"), "Login error")


class _LoginSignUpComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def name(self):
        return Input(self.__root.element("[data-qa=signup-name]"), "Name")

    def email(self):
        return Input(self.__root.element("[data-qa=signup-email]"), "Email")

    def submit(self):
        return Button(self.__root.element("[data-qa=signup-button]"), "Sign Up")


class _SignUpComponentLocator:

    def __init__(self, root: Element):
        self.__root = root

    def user_titles_wrapper(self) -> UiElement:
        return UiElement(self.__root.element(".clearfix"), "User Titles container")

    def user_titles(self) -> RadioButtons:
        return RadioButtons(self.__root.all(".radio"), "User Titles")

    def name(self) -> Input:
        return Input(self.__root.element("#name"), "Name")

    def email(self) -> Input:
        return Input(self.__root.element("#email"), "Email")

    def password(self) -> Input:
        return Input(self.__root.element("#password"), "Password")

    def birth_day(self) -> Select:
        return Select(self.__root.element("#days"), "Birth Day")

    def birth_month(self) -> Select:
        return Select(self.__root.element("#months"), "Birth Month")

    def birth_year(self) -> Select:
        return Select(self.__root.element("#years"), "Birth Year")

    def newsletter(self) -> Checkbox:
        return Checkbox(self.__root.element("#newsletter"), "Newsletter")

    def special_offers(self) -> Checkbox:
        return Checkbox(self.__root.element("#optin"), "Special Offers")

    def first_name(self) -> Input:
        return Input(self.__root.element("#first_name"), "First Name")

    def last_name(self) -> Input:
        return Input(self.__root.element("#last_name"), "Last Name")

    def company(self) -> Input:
        return Input(self.__root.element("#company"), "Company")

    def address1(self) -> Input:
        return Input(self.__root.element("#address1"), "Address 1")

    def address2(self) -> Input:
        return Input(self.__root.element("#address2"), "Address 2")

    def country(self) -> Select:
        return Select(self.__root.element("#country"), "Country")

    def state(self) -> Input:
        return Input(self.__root.element("#state"), "State")

    def city(self) -> Input:
        return Input(self.__root.element("#city"), "City")

    def zip_code(self) -> Input:
        return Input(self.__root.element("#zipcode"), "Zip Code")

    def mobile_number(self) -> Input:
        return Input(self.__root.element("#mobile_number"), "Mobile Number")

    def submit(self) -> Button:
        return Button(self.__root.element("button[data-qa=create-account]"), "Submit")
