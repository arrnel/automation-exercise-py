import pytest

from src.util.data_generator import DataGenerator
from tests.web.base_test import BaseWebTest


@pytest.mark.web_test
class TestSubscriptionComponent(BaseWebTest):

    @pytest.mark.screenshot_test
    def test_subscription_component_has_expected_screenshot(self, browser_open):
        # Step & Assertion
        self.login_page.subscription.check_component_has_screenshot("files/screenshot/component/subscription/empty_subscription.png")

    @pytest.mark.screenshot_test
    def test_should_subscribe_with_valid_email(self, browser_open):
        # Steps
        self.login_page.subscription.subscribe(DataGenerator.generate_email())

        # Assertion
        self.login_page.subscription.check_subscribe_status_message_is_visible()
        self.login_page.subscription.check_component_has_screenshot(
            "files/screenshot/component/subscription/subscribe_with_valid_email.png"
        )

    @pytest.mark.screenshot_test
    def test_should_not_subscribe_with_invalid_email(self, browser_open):
        # Steps
        self.login_page.subscription.subscribe(DataGenerator.generate_invalid_email())

        # Assertion
        self.login_page.subscription.check_subscribe_status_message_is_visible()
        self.login_page.subscription.check_component_has_screenshot(
            "files/screenshot/component/subscription/subscribe_with_invalid_email.png"
        )
