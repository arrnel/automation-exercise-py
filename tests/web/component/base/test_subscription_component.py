import allure
import pytest

from src.util.email_util import EmailUtil
from tests.web.base_test import BaseWebTest

_INVALID_EMAIL_TEXT = "Invalid email"

@pytest.mark.web_test
class TestSubscriptionComponent(BaseWebTest):

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Subscription component")
    @allure.title("[WEB Component] Subscription component should have expected screenshot")
    def test_subscription_component_has_expected_screenshot(self):
        # Step & Assertion
        self.main_page.subscription.check_component_has_screenshot("files/screenshot/component/subscription/empty_subscription.png")

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Subscription component")
    @allure.title("[WEB Component] Should subscribe with valid email")
    def test_should_subscribe_with_valid_email(self):
        # Steps
        self.main_page.subscription.subscribe(EmailUtil.invalid_email().random())

        # Assertion
        self.main_page.subscription.check_subscribe_has_success_status_message()
        self.main_page.subscription.check_component_has_screenshot(
            "files/screenshot/component/subscription/subscribe_with_valid_email.png"
        )

    @pytest.mark.screenshot_test
    @allure.tag("screenshot_test")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Subscription component")
    @allure.title("[WEB Component] Should not subscribe with invalid email")
    def test_should_not_subscribe_with_invalid_email(self):
        # Steps
        self.main_page.subscription.subscribe(EmailUtil.invalid_email().random())

        # Assertion
        self.main_page.subscription.check_success_subscribe_status_message_has_text(_INVALID_EMAIL_TEXT)
        self.main_page.subscription.check_component_has_screenshot(
            "files/screenshot/component/subscription/subscribe_with_invalid_email.png"
        )
