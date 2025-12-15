from selene import browser

from src.ui.component.auth_component import LoginComponent, LoginSignUpComponent
from src.ui.page.base_page import BasePage
from src.util.allure.step_logger import step_log

_URL = "/login"

class LoginPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__login_component = LoginComponent(self._page_container.element(".login-form"))
        self.__sign_up_component = LoginSignUpComponent(self._page_container.element(".signup-form"))

    # COMPONENTS
    @property
    def login_component(self) -> LoginComponent:
        return self.__login_component

    @property
    def sign_up_component(self) -> LoginSignUpComponent:
        return self.__sign_up_component

    # ACTIONS
    @step_log.log("Open [Login Page]: {_URL}")
    def navigate(self) -> None:
        browser.open(_URL)

    # ASSERTIONS
    @step_log.log("Check [{self._page_name}] is visible")
    def check_page_is_visible(self):
        self.__login_component.check_component_is_visible()
        self.__sign_up_component.check_component_is_visible()

    @step_log.log("Check [{self._page_name}] is not visible")
    def check_page_is_not_visible(self):
        self.__login_component.check_component_is_not_exists()
        self.__sign_up_component.check_component_is_not_exists()
