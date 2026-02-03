from typing import TypeVar

from src.client.core.condition.base import Condition
from src.client.core.condition.body_condition import (
    BodyFieldEqualsCondition,
    BodyArrayContainsCondition,
    BodyArrayHasCondition,
    BodyArrayHasOrderedCondition,
    BodyArrayNotContainsCondition,
    BodyArrayHasSizeCondition,
    BodyArrayIsEmptyCondition,
    BodyFieldExistsCondition,
    BodyFieldNotEqualsCondition,
)
from src.client.core.condition.cookie_condition import (
    CookieExistsCondition,
    CookiesHasValueCondition,
)
from src.client.core.condition.header_condition import (
    ContentTypeCondition,
    HeadersExistCondition,
)
from src.client.core.condition.status_code_condition import StatusCodeCondition
from src.model.enum.meta.content_type import ContentType

T = TypeVar("T")


class Conditions:

    @staticmethod
    def status_code(status_code: int) -> Condition:
        """Example: .status_code(HTTPStatus.OK)"""
        return StatusCodeCondition(status_code)

    @staticmethod
    def content_type(content_type: ContentType) -> Condition:
        """Example: .content_type(ContentType.JSON)"""
        return ContentTypeCondition(content_type)

    @staticmethod
    def headers_exists(*headers: str) -> Condition:
        """Example: .headers_exists("Location", "User-Agent")"""
        return HeadersExistCondition(*headers)

    @staticmethod
    def headers_has_value(*headers: str) -> Condition:
        """Example: .headers_has_value(**{"Location": "https://example.com"})"""
        return HeadersExistCondition(*headers)

    @staticmethod
    def cookies_exists(*cookies: str) -> Condition:
        """Example: .cookies_exists("sessionid", "csrf")"""
        return CookieExistsCondition(*cookies)

    @staticmethod
    def cookies_has_value(**cookies) -> Condition:
        """Example: .cookies_has_value(sessionid="session_id_example", csrf="csrf_example")"""
        return CookiesHasValueCondition(**cookies)

    @staticmethod
    def body_field_exists(path: str) -> Condition:
        """Example: .body_field("user.id", 1)"""
        return BodyFieldExistsCondition(path)

    @staticmethod
    def body_field_equals(path: str, expected_value) -> Condition:
        """Example: .body_field("user.id", 1)"""
        return BodyFieldEqualsCondition(path, expected_value)

    @staticmethod
    def body_field_not_equals(path: str, expected_value, *expected_values) -> Condition:
        """Example: .body_field("user.id", 1)"""
        return BodyFieldNotEqualsCondition(path, expected_value, *expected_values)

    @staticmethod
    def body_status_code(status_code: int) -> Condition:
        """Example: .body_status_code(HTTPStatus.OK)"""
        return BodyFieldEqualsCondition("responseCode", status_code)

    @staticmethod
    def body_array_has_size(path: str, count: int) -> Condition:
        """Example: .body_array_contains_values("users[*].id", 1, 2, 5)"""
        return BodyArrayHasSizeCondition(path, count)

    @staticmethod
    def body_array_is_empty(path: str) -> Condition:
        """Example: .body_array_contains_values("users[*].id", 1, 2, 5)"""
        return BodyArrayIsEmptyCondition(path)

    @staticmethod
    def body_array_contains_values(
        path: str, expected_value: T, *expected_values: T
    ) -> Condition:
        """Example: .body_array_contains_values("users[*].id", 1, 2, 5)"""
        return BodyArrayContainsCondition(path, expected_value, *expected_values)

    @staticmethod
    def body_array_not_contains_values(
        path: str, expected_value: T, *expected_values: T
    ) -> Condition:
        """Example: .body_array_contains_values("users[*].id", 1, 2, 5)"""
        return BodyArrayNotContainsCondition(path, expected_value, *expected_values)

    @staticmethod
    def body_array_has_values(path: str, expected_value, expected_values) -> Condition:
        """Example: .body_array_has_values("users[*].id", 1, 2, 5)"""
        return BodyArrayHasCondition(path, expected_value, expected_values)

    @staticmethod
    def body_array_has_ordered_values(
        path: str, expected_value, expected_values
    ) -> Condition:
        """Example: .body_array_has_ordered_values("users[*].id", 1, 2, 5)"""
        return BodyArrayHasOrderedCondition(path, expected_value, expected_values)
