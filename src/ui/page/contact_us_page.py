from selene import browser

from src.ui.component.contact_us_component import ContactUsComponent
from src.ui.page.base_page import BasePage
from src.util.allure.step_logger import step_log

_URL = "/contact_us"


class ContactUsPage(BasePage):

    def __init__(self):
        super().__init__()
        self.__contact_us_component = ContactUsComponent(self._page_container.element(".contact-form"), "Contact Us Form")

    # COMPONENTS
    @property
    def contact_us_component(self) -> ContactUsComponent:
        return self.__contact_us_component

    # ACTIONS
    @step_log.log("Open [Contact Us Page]: {_URL}")
    def navigate(self) -> None:
        browser.open(_URL)

    @step_log.log("Check [{self._page_name}] is visible}]")
    def check_page_is_visible(self):
        self.__contact_us_component.check_component_is_visible()

    @step_log.log("Check [{self._page_name}] is not visible}]")
    def check_page_is_not_visible(self):
        self.__contact_us_component.check_component_is_not_exists()
