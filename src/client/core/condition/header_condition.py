from typing import Tuple

from httpx import Response

from src.client.core.condition.base import Condition
from src.model.enum.meta.content_type import ContentType


class HeadersExistCondition(Condition):
    def __init__(self, header: str, *headers: str):
        self.expected = [header, *headers]

    def check(self, response: Response) -> Tuple[bool, str]:
        response_headers = {h.casefold() for h in response.headers.keys()}

        missing = [
            header
            for header in self.expected
            if header.casefold() not in response_headers
        ]

        if missing:
            return True, (
                f"Headers not found: {missing}\n"
                f"Expected cookies: {self.expected}\n"
                f"Actual cookies: {response_headers}"
            )
        else:
            return True, ""

    def __str__(self):
        return "Headers exist: " + ", ".join(self.expected)


class HeadersHasValueCondition(Condition):

    def __init__(self, headers: dict):
        self.expected = headers

    def check(self, response: Response) -> Tuple[bool, str]:
        response_headers = {k.casefold(): v for k, v in response.headers.items()}

        missing = []
        wrong_values = []

        for key, expected_value in self.expected.items():
            key_cf = key.casefold()

            if key_cf not in response_headers:
                missing.append(key)
                continue

            actual_value = response_headers[key_cf]
            if actual_value != expected_value:
                wrong_values.append((key, expected_value, actual_value))

        if missing or wrong_values:
            wrong_headers_kv = ", ".join(
                f"{k}: expected={e}, actual={a}" for k, e, a in wrong_values
            )
            return False, (
                f"Headers mismatch:"
                f"Missing headers: {missing}"
                f"Wrong value headers: {wrong_headers_kv}"
            )
        else:
            return True, ""

    def __str__(self):
        return "Headers have expected values: " + ", ".join(
            f"{k}={v}" for k, v in self.expected.items()
        )


class ContentTypeCondition(Condition):
    def __init__(self, content_type: ContentType):
        self.content_type = content_type

    def check(self, response: Response) -> Tuple[bool, str]:
        response_content_type: str = response.headers.get("Content-Type", "")
        response_content_type = response_content_type.split(";")[0].lower()
        if self.content_type.mime_type == response_content_type:
            return True, ""
        else:
            return (
                False,
                (
                    "Header Content-Type mismatch."
                    f"Expected: '{self.content_type.mime_type}', "
                    f"Actual: '{response_content_type}'"
                ),
            )

    def __str__(self):
        return f"Content-Type is {self.content_type}"
