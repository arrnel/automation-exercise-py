from selene import browser

from src.ui.component.auth_component import LoginComponent, LoginSignUpComponent
from src.ui.page.base_page import BasePage
from src.util.decorator.step_logger import step_log

URL = "/login"


class LoginPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__login_component = LoginComponent(
            self._page_container.element(".login-form")
        )
        self.__pre_sign_up_component = LoginSignUpComponent(
            self._page_container.element(".signup-form")
        )

    # COMPONENTS
    @property
    def login_component(self) -> LoginComponent:
        return self.__login_component

    @property
    def pre_sign_up_component(self) -> LoginSignUpComponent:
        return self.__pre_sign_up_component

    # ACTIONS
    @step_log.log("Open [Login Page]: {URL}")
    def navigate(self) -> None:
        browser.open(URL)

    # ASSERTIONS
    @step_log.log("Check [{self._page_name}] is visible")
    def check_page_is_visible(self):
        self.__login_component.check_component_is_visible()
        self.__pre_sign_up_component.check_component_is_visible()

    @step_log.log("Check [{self._page_name}] is not visible")
    def check_page_is_not_visible(self):
        self.__login_component.check_component_is_not_exists()
        self.__pre_sign_up_component.check_component_is_not_exists()
