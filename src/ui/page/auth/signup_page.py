from src.ui.component.auth_component import SignUpComponent
from src.ui.page.base_page import BasePage


class SignUpPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__sign_up_component = SignUpComponent(
            self._page_container.element(".login-form"),
            "Sign Up Account Information form",
        )

    # COMPONENTS
    @property
    def sign_up_component(self):
        return self.__sign_up_component

    # ASSERTIONS
    def check_page_is_visible(self):
        self.__sign_up_component.check_component_is_visible()

    def check_page_is_not_visible(self):
        self.__sign_up_component.check_component_is_not_exists()
