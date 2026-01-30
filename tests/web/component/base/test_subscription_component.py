import allure
import pytest

from src.util.decorator.disabled_by_issue import disabled_by_issue
from src.util.email_util import EmailUtil
from src.util.test.data_generator import DataGenerator
from tests.web.base_web_component_test import BaseWebComponentTest

_INVALID_EMAIL_TEXT = "Invalid email"


@pytest.mark.component_test
@pytest.mark.subscription_component_test
@allure.feature("Subscription Component")
class TestSubscriptionComponent(BaseWebComponentTest):

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Subscription component")
    @allure.title(
        "[WEB Component] Subscription component should have expected screenshot"
    )
    def test_subscription_component_has_expected_screenshot(self):
        # Step & Assertion
        self.main_page.subscription.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/subscription/empty_subscription.png"
        )

    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Subscription component")
    @allure.title("[WEB Component] Should subscribe with valid email")
    def test_should_subscribe_with_valid_email(self):
        # Steps
        self.main_page.subscription.subscribe(EmailUtil.valid_email().random())

        # Assertion
        self.main_page.subscription.check_subscribe_has_success_status_message()
        self.main_page.subscription.check_component_with_status_message_has_screenshot(
            "files/screenshot/component/subscription/subscribe_with_valid_email.png"
        )

    @disabled_by_issue(issue_id=1, reason="[WEB] Not validate email address")
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Subscription component")
    @allure.title("[WEB Component] Should not subscribe with invalid email")
    def test_should_not_subscribe_with_invalid_email(self):
        # Steps
        self.main_page.subscription.subscribe(EmailUtil.invalid_email().random())

        # Assertion
        self.main_page.subscription.check_success_subscribe_status_message_has_text(
            _INVALID_EMAIL_TEXT
        )
        self.main_page.subscription.check_component_with_status_message_has_screenshot(
            "files/screenshot/component/subscription/subscribe_with_invalid_email.png"
        )

    @pytest.mark.usefixtures("open_contact_us_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Subscription component")
    @allure.title(
        "[WEB Component] Should have expected success status message after sending contact info"
    )
    def test_should_have_success_subscription_status_message_after_sending_contact_form(
        self,
    ):
        # Data
        contact_info = DataGenerator.random_contact_info()

        # Steps
        self.contact_us_page.contact_us_component.send(contact_info)
        self.contact_us_page.subscription.subscribe(contact_info.email)

        # Assertion
        self.contact_us_page.subscription.check_subscribe_has_success_status_message()
