from collections.abc import Iterable
from typing import Type, TypeVar, List, Any

import six
from httpx import Response

from src.ex.exception import (
    DeserializationError,
)
from src.util.api.json_path_util import matches_by_json_path

T = TypeVar("T")


class Extractor:

    def __init__(self, response: Response):
        self.response = response

    def status_code(self) -> int:
        return self.response.status_code

    def body_status_code(self) -> int:
        return self.as_value("responseCode")

    def cookie(self, title: str) -> str:
        return self.response.cookies.get(title)

    def cookies(self, titles: list[str] = None) -> dict[str, str]:
        if titles is None or not titles:
            titles = self.response.cookies.keys()
        return {title: self.response.cookies.get(title) for title in titles}

    def as_value(self, json_path: str) -> Any:
        """
        Extract vars or objects from json. Examples:
        .as_value("responseStatus") - extract response status
        .as_value("users[0].first_name") - extract first user first name
        """
        matches = matches_by_json_path(self.response.json(), json_path)
        if not matches:
            raise KeyError(f"Not found in json key by json path: {json_path}")
        if len(matches) > 1:
            raise ValueError(f"Found multiple matches by json path: {json_path}")
        return matches[0]

    def as_pojo(self, cls: Type[T], path: str = None) -> T:
        """
        Extract vars or objects from json. Examples:
        .as_pojo(cls=UserResponseDTO, path="users[0]") - extract first user as UserDTO
        """
        self.__validate_path_not_contains_array_symbol(path)
        self.__validate_cls_not_collection(cls)

        matches = matches_by_json_path(self.response.json(), path)
        if not matches:
            raise KeyError(f"Not found in json key by path: {path}")
        if len(matches) > 1:
            raise ValueError(
                f"Found multiple matches by path: {path}\n. Matches: {matches}"
            )
        try:
            return cls(**matches[0])
        except Exception as ex:
            raise DeserializationError(
                f"Unable to deserialize as type = [{cls}] by match: {matches[0]}.\nException: {ex}"
            )

    def as_list(self, cls: Type[T], path: str = None) -> List[T]:
        """
        Extract vars or objects as list from json. Examples:
        .as_list(ProductResponseDTO, "products[*]") - extract products as list[ProductResponseDTO],
        .as_list(cls = str, path "users[*].first_name") - extract users first_name as list[str]
        """
        self.__validate_path_contains_array_symbol(path)
        self.__validate_cls_not_collection(cls)

        data = (
            self.response.json()
            if path is None
            else matches_by_json_path(self.response.json(), path)
        )
        if not isinstance(data, Iterable) or isinstance(data, six.string_types):
            raise TypeError(
                f"JSONPath '{path}' returns {type(data)}. Expected: List[{cls.__name__}]"
            )
        try:
            if self.__is_primitive(cls):
                return [cls(item) for item in data]
            else:
                return [cls(**item) for item in data]
        except Exception as ex:
            raise DeserializationError(
                f"Unable to deserialize as type = List[{cls}] by match: {data}.\nException: {ex}"
            )

    def as_json(self) -> dict:
        return self.response.json()

    def content_as_bytes(self) -> bytes:
        return self.response.content

    def __validate_cls_not_collection(self, cls: type[T]):
        if isinstance(cls, Iterable) and not isinstance(cls, six.string_types):
            raise TypeError("Argument `cls` should not be a collection")

    def __validate_path_not_contains_array_symbol(self, path: str | None):
        if path.__contains__("[*]"):
            raise ValueError("Invalid path. Path should not contains: `[*]`")

    def __validate_path_contains_array_symbol(self, path: str | None):
        if not path.__contains__("[*]"):
            raise ValueError("Invalid path. Path should contains: `[*]`")

    def __is_primitive(self, cls: Type[T]):
        return cls in (str, int, float, bool)
