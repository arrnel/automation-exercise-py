from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, List


@dataclass
class DiffTableRow:
    title: str
    expected: Any
    actual: Any


class DiffTable:

    def __init__(
            self,
            values: Iterable[DiffTableRow],
            keys_column_length: int = 16,
            values_column_length: int = 14,
    ):
        self.__separator_tpl = (
            f"+{'-' * keys_column_length}"
            f"+{'-' * values_column_length}"
            f"+{'-' * values_column_length}+\n"
        )
        self.__row_tpl = (
            f"|{{:<{keys_column_length}}}"
            f"|{{:<{values_column_length}}}"
            f"|{{:<{values_column_length}}}|\n"
        )
        self.__diff_table = self.__build_diff_table(values)

    @property
    def diff_table(self) -> str:
        return self.__diff_table

    def __build_diff_table(self, values: Iterable[DiffTableRow]) -> str:
        diff_list: List[str] = []
        self.__append_separator(diff_list)
        self.__append_row(diff_list, "", "Expected", "Actual")
        self.__append_separator(diff_list)
        for value in values:
            self.__append_row(diff_list, value.title, value.expected, value.actual)
            self.__append_separator(diff_list)
        return "".join(diff_list)

    def __append_separator(self, diff_list: List[str]):
        diff_list.append(self.__separator_tpl)

    def __append_row(self, diff_list, label: str, expected, actual):
        diff_list.append(self.__row_tpl.format(label, str(expected), str(actual)))
