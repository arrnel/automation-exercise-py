import json
from typing import Optional

import allure
from PIL import Image
from allure_commons.types import AttachmentType
from httpx import Request, Response

from src.model.enum.meta.content_type import ContentType
from src.model.enum.meta.log_level import ApiLogLvl
from src.util.api.httpx_log_formatter_util import format_response, format_request
from src.util.screenshot import image_util

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
                "expected": f"{_BASE64_PNG_INCEPTION}{image_util.get_img_base64(expected_screenshot)}",
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
