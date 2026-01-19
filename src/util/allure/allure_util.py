import json
from typing import Optional

import allure
from PIL import Image
from allure_commons.types import AttachmentType
from httpx import Request, Response
from selene import browser

from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType
from src.model.enum.meta.log_level import ApiLogLvl
from src.service.remote import remote_artifact_factory
from src.util.api.httpx_log_formatter_util import format_response, format_request
from src.util.screenshot import image_util
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore

_JSON_CONTENT_TYPES = ["application/json", "application/vnd.github+json"]
_BASE64_PNG_INCEPTION = "data:image/png;base64,"


class AllureUtil:

    @staticmethod
    def attach_request(
        request: Request,
        api_log_lvl: ApiLogLvl = Optional[ApiLogLvl],
        attachment_type: AttachmentType = Optional[AttachmentType],
    ) -> None:
        attachment_type = attachment_type or ContentType.from_mime(
            request.headers.get("Content-Type")
        )
        allure.attach(
            format_request(request, api_log_lvl),
            "Request",
            attachment_type,
        )

    @staticmethod
    def attach_response(
        response: Response,
        api_log_lvl: ApiLogLvl = Optional[ApiLogLvl],
        attachment_type: AttachmentType = Optional[AttachmentType],
    ) -> None:
        attachment_type = attachment_type or ContentType.from_mime(
            response.headers.get("Content-Type")
        )
        allure.attach(
            format_response(response, api_log_lvl),
            "Response",
            attachment_type,
        )

    @staticmethod
    def attach_screen_diff(
        expected_screenshot: Image.Image,
        actual_screenshot: Image.Image,
        diff_image: Image.Image,
    ) -> None:
        content = json.dumps(
            {
                "expected": (
                    f"{_BASE64_PNG_INCEPTION}"
                    f"{image_util.get_img_base64(expected_screenshot)}"
                ),
                "actual": f"{_BASE64_PNG_INCEPTION}{image_util.get_img_base64(actual_screenshot)}",
                "diff": f"{_BASE64_PNG_INCEPTION}{image_util.get_img_base64(diff_image)}",
            }
        ).encode()

        allure.attach(
            content,
            name="Screenshot diff",
            attachment_type="application/vnd.allure.image.diff",
        )

    @staticmethod
    def attach_screen_diff_table(diff_table: str) -> None:
        allure.attach(
            name="Screenshot diff data table",
            body=diff_table,
            attachment_type=AttachmentType.TEXT,
        )

    @staticmethod
    def attach_screenshot() -> None:
        screenshot = browser.driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name="Screenshot",
            attachment_type=AttachmentType.PNG,
        )

    @staticmethod
    def attach_page_source() -> None:
        page_source = browser.driver.page_source
        allure.attach(
            page_source,
            name="Page Source",
            attachment_type=AttachmentType.HTML,
        )

    @staticmethod
    def attach_test_video() -> None:

        if CFG.browser_remote_video_id_type == "test_name":
            test_id = ThreadSafeTestThreadsStore().current_thread_test_name()
        else:
            test_id = browser.driver.session_id

        content = remote_artifact_factory.instance().get_video(test_id)

        allure.attach(
            content,
            name="Test video",
            attachment_type=AttachmentType.MP4,
        )
