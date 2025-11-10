from typing import Type, TypeVar, List, Any

from httpx import Response

from src.ex.exception import (
    DeserializationError,
)
from src.util.json_path_util import matches_by_json_path

T = TypeVar("T")


class Extractor:

    def __init__(self, response: Response):
        self.response = response

    def body_status_code(self) -> int:
        return self.as_value("statusCode")

    def cookie(self, title: str) -> str:
        return self.response.cookies.get(title)

    def cookies(self, titles: list[str] = None) -> dict[str, str]:
        if titles is None or not titles:
            titles = self.response.cookies.keys()
        return {title: self.response.cookies.get(title) for title in titles}

    def as_value(self, json_path: str) -> Any:
        matches = matches_by_json_path(self.response.json(), json_path)
        if not matches:
            raise KeyError(f"Not found in json key by json path: {json_path}")
        if len(matches) > 1:
            raise ValueError(f"Found multiple matches by json path: {json_path}")
        return matches[0]

    def as_pojo(self, cls: Type[T], path: str = None) -> T:

        self.__validate_path_not_contains_array_symbol(path)
        self.__validate_cls_not_list(cls)

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

        self.__validate_cls_not_list(cls)

        data = (
            self.response.json()
            if path is None
            else matches_by_json_path(self.response.json(), path)
        )
        if not isinstance(data, list):
            raise TypeError(
                f"JSONPath '{path}' returns {type(data)}. Expected: List[{cls.__name__}]"
            )
        try:
            return [cls(**item) for item in data]
        except Exception as ex:
            raise DeserializationError(
                f"Unable to deserialize as type = List[{cls}] by match: {data}.\nException: {ex}"
            )

    def __validate_cls_not_list(self, cls: type[T]):
        if isinstance(cls, list):
            raise TypeError("Argument `cls` should not be a list")

    def __validate_path_not_contains_array_symbol(self, path: str | None):
        if path.__contains__("[*]"):
            raise ValueError("Invalid path. Path should not contains: `[*]`")
