from typing import Optional

import allure
from allure_commons.types import AttachmentType
from httpx import Request, Response

from src.model.enum.meta.content_type import ContentType
from src.model.enum.meta.log_level import ApiLogLvl
from src.util.httpx_log_formatter_util import format_response, format_request

_JSON_CONTENT_TYPES = ["application/json", "application/vnd.github+json"]


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
