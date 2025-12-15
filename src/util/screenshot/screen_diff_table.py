import json
from dataclasses import dataclass
from typing import Any, List

import allure
import numpy as np
from PIL import Image

from src.util.screenshot.image_util import get_img_base64, colored_diff_image, normalize_images, get_diff_image

_MAX_PERCENT_OF_TOLERANCE = 0.2


class ScreenDiffResult:

    def __init__(self, expected: Image.Image, actual: Image.Image, percent_of_tolerance: float = 0.0):

        if not (0.0 <= percent_of_tolerance <= _MAX_PERCENT_OF_TOLERANCE):
            raise ValueError(
                f"Illegal percent of tolerance value. Allowed between [0, {_MAX_PERCENT_OF_TOLERANCE}]"
            )

        self.__expected = expected
        self.__actual = actual
        self.__percent_of_tolerance = percent_of_tolerance
        self.__has_diff = self.__calculate_diff()

    @property
    def has_diff(self) -> bool:
        return self.__has_diff

    def __calculate_diff(self) -> bool:

        def calculate_diff_pixels(image: Image.Image) -> int:
            diff_array = np.array(image)
            if len(diff_array.shape) == 3:  # Для многоканальных изображений
                actual_diff_size = np.count_nonzero(np.any(diff_array != 0, axis=-1))
            else:
                actual_diff_size = np.count_nonzero(diff_array)
            return int(actual_diff_size)

        screen_pixels = self.__expected.width * self.__expected.height
        n_exp_img, n_act_img = normalize_images(self.__expected, self.__actual)
        diff_image = get_diff_image(n_exp_img, n_act_img)

        self.__expected_diff_size = int(round(screen_pixels * self.__percent_of_tolerance))
        self.__actual_diff_size = calculate_diff_pixels(diff_image)
        self.__actual_diff_percent = self.__actual_diff_size / screen_pixels

        self.__colored_diff_image = colored_diff_image(n_exp_img, diff_image)

        self.__diff_table = ScreenDiffTable(
            expected_diff_size=self.__expected_diff_size,
            expected_diff_percent=self.__percent_of_tolerance,
            actual_diff_size=self.__actual_diff_size,
            actual_diff_percent=self.__actual_diff_percent,
        ).diff_table

        return self.__actual_diff_size > self.__expected_diff_size

    def attach_diff_to_allure(self):
        content = json.dumps(
            {
                "expected": f"data:image/png;base64,{get_img_base64(self.__expected)}",
                "actual": f"data:image/png;base64,{get_img_base64(self.__actual)}",
                "diff": f"data:image/png;base64,{get_img_base64(self.__colored_diff_image)}",
            }
        )
        allure.attach(
            content,
            name="Screenshot diff",
            attachment_type="application/vnd.allure.image.diff",
        )
        allure.attach(name="Screenshot diff data table", body=self.__diff_table)


class ScreenDiffTable:
    __keys_column_length = 16
    __values_column_length = 14

    __separator_tpl = f"+{'-' * __keys_column_length}+{'-' * __values_column_length}+{'-' * __values_column_length}+\n"
    __row_tpl = f"|{{:<{__keys_column_length}}}|{{:<{__values_column_length}}}|{{:<{__values_column_length}}}|\n"

    def __init__(
            self,
            expected_diff_size: int,
            actual_diff_size: int,
            expected_diff_percent: float,
            actual_diff_percent: float,
    ):
        self.__diff_table = self.__build_diff_table([
            DiffTableRow("diff_size", expected_diff_size, actual_diff_size),
            DiffTableRow("diff_percent", expected_diff_percent, actual_diff_percent),
        ])

    @property
    def diff_table(self) -> str:
        return self.__diff_table

    def __build_diff_table(self, values: List["DiffTableRow"]) -> str:
        diff_table: List[str] = []
        self.__append_separator(diff_table)
        self.__append_row(diff_table, "", "Expected", "Actual")
        for value in values:
            self.__append_row(diff_table, value.title, value.expected, value.actual)
            self.__append_separator(diff_table)
        return "".join(self.diff_table)

    def __append_separator(self, diff_table: List[str]):
        diff_table.append(self.__separator_tpl)

    def __append_row(self, diff_table, label: str, expected:T, actual:T):
        values = []
        diff_table.append(self.__row_tpl.format(label, str(expected), str(actual)))


@dataclass
class DiffTableRow:
    title: str
    expected: Any
    actual: Any
