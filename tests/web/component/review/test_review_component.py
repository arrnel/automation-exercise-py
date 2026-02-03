import allure
import pytest

from src.model.review import ReviewInfo
from src.util.decorator.disabled_by_issue import disabled_by_issue
from tests.data_provider.review_data_provider import ReviewDataProviderUI
from tests.web.base_web_component_test import BaseWebComponentTest


@pytest.mark.component_test
@pytest.mark.review_component_test
@allure.feature("Review Component")
class TestReviewComponent(BaseWebComponentTest):

    @pytest.mark.usefixtures("open_product_page")
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Review Component")
    @allure.title("[WEB] Should have expected screenshot when not send review")
    def test_should_have_expected_screenshot_when_not_send_review(self):
        # Assertion
        self.product_page.review.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/review/review_not_send.png",
        )

    @pytest.mark.usefixtures("open_expected_product_page")
    @pytest.mark.screenshot_test
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Review Component")
    @allure.title("[WEB] Should have expected screenshot when send review")
    def test_should_have_expected_screenshot_when_send_review(self):
        # Component
        review_component = self.product_page.review

        # Data
        review_info = ReviewInfo("Ivan Ivanov", "test@test.test", "Good item")

        # Steps
        review_component.send_review(review_info)

        # Assertion
        review_component.check_component_has_screenshot(
            path_to_screenshot="files/screenshot/component/review/review_send.png",
        )

    @pytest.mark.usefixtures("open_expected_product_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Review Component")
    @pytest.mark.parametrize(
        "case_title, review",
        ReviewDataProviderUI.valid_data_provider(),
        ids=[param[0] for param in ReviewDataProviderUI.valid_data_provider()],
    )
    @allure.title("[WEB] Should add product review with valid data. Case: {case_title}")
    def test_add_review_with_valid_data(self, case_title: str, review: ReviewInfo):
        # Component
        review_component = self.product_page.review

        # Steps
        review_component.send_review(review)

        # Assertion
        self.product_page.review.check_review_status_message_successful()

    @disabled_by_issue(issue_id=3, reason="[WEB] Not validate sensitive data")
    @pytest.mark.usefixtures("open_expected_product_page")
    @allure.label("owner", "arrnel")
    @allure.story("[Web] Component - Review Component")
    @pytest.mark.parametrize(
        "case_title, review, error_message",
        ReviewDataProviderUI.invalid_data_provider(),
        ids=[param[0] for param in ReviewDataProviderUI.invalid_data_provider()],
    )
    @allure.title(
        "[WEB] Should not add product review with invalid data. Case: {case_title}"
    )
    def test_not_add_review_with_invalid_data(
        self,
        case_title: str,
        review: ReviewInfo,
        error_message: str,
    ):
        # Component
        review_component = self.product_page.review

        # Steps
        review_component.send_review(review)

        # Assertion
        review_component.check_review_status_message_has_text(error_message)
