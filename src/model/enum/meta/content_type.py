from enum import Enum
from typing import Optional

from allure_commons.types import AttachmentType


class ContentType(Enum):

    def __init__(self, mime_type, attachment_type):
        self.mime_type: str = mime_type
        self.attachment_type: AttachmentType = attachment_type

    JSON = ("application/json", AttachmentType.JSON)
    GITHUB_JSON = ("application/vnd.github+json", AttachmentType.JSON)
    URL_ENCODED = ("application/x-www-form-urlencoded", AttachmentType.TEXT)
    HTML = ("text/html", AttachmentType.HTML)
    TEXT = ("text/plain", AttachmentType.TEXT)

    @staticmethod
    def from_mime(mime: str, default: "ContentType" = None) -> Optional["ContentType"]:
        if mime is None:
            return default

        for content_type in ContentType:
            if mime.lower() == content_type.mime_type:
                return content_type

        return default
