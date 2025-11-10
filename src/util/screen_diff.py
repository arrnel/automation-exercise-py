import json
from decimal import Decimal

import allure
import numpy as np
from PIL import Image

from src.util.image_util import get_img_base64, get_diff_image

_MAX_PERCENT_OF_TOLERANCE = 0.2


class ScreenDiffResult:

    def __init__(
        self, expected: Image.Image, actual: Image.Image, percent_of_tolerance: float
    ):

        if not (0.0 <= percent_of_tolerance <= _MAX_PERCENT_OF_TOLERANCE):
            raise ValueError(
                f"Illegal percent of tolerance value. Allowed between [0, {_MAX_PERCENT_OF_TOLERANCE}]"
            )

        self.__expected = expected
        self.__actual = actual
        self.__percent_of_tolerance = percent_of_tolerance
        self.__has_diff = self.__calculate_diff()

    def __calculate_diff(self) -> bool:

        screen_pixels = self.__expected.width * self.__expected.height
        diff_image = get_diff_image(
            expected_screenshot=self.__expected, actual_screenshot=self.__actual
        )
        expected_diff_size = int(
            round(screen_pixels * Decimal.from_float(self.__percent_of_tolerance))
        )
        actual_diff_size = self.calculate_diff_pixels(diff_image=diff_image)
        has_diff = actual_diff_size > expected_diff_size

        if has_diff:
            content = json.dumps(
                {
                    "expected": f"data:image/png;base64,{get_img_base64(self.__expected)}",
                    "actual": f"data:image/png;base64,{get_img_base64(self.__actual)}",
                    "diff": f"data:image/png;base64,{get_img_base64(diff_image)}",
                }
            )
            self.__diff_data_table = ScreenDiffTable(
                expected_diff_size=expected_diff_size,
                actual_diff_size=actual_diff_size,
                expected_diff_percent=self.__percent_of_tolerance,
                actual_diff_percent=actual_diff_size / screen_pixels,
            ).get_diff_table()
            allure.attach(
                content,
                name="Screenshot diff",
                attachment_type="application/vnd.allure.image.diff",
            )
            allure.attach(name="Screenshot diff data", body=self.__diff_data_table)

        return has_diff

    def calculate_diff_pixels(self, diff_image: Image.Image) -> int:
        diff_array = np.array(diff_image)
        if len(diff_array.shape) == 3:  # Для многоканальных изображений
            actual_diff_size = np.count_nonzero(np.any(diff_array != 0, axis=-1))
        else:
            actual_diff_size = np.count_nonzero(diff_array)
        return int(actual_diff_size)

    def has_diff(self) -> bool:
        return self.__has_diff

    def calculate_diff_pixels(self, diff_image: Image.Image) -> int:
        diff_array = np.array(diff_image)
        if len(diff_array.shape) == 3:  # Для многоканальных изображений
            actual_diff_size = np.count_nonzero(np.any(diff_array != 0, axis=-1))
        else:
            actual_diff_size = np.count_nonzero(diff_array)
        actual_diff_size = int(actual_diff_size)
        return actual_diff_size

    def has_diff(self) -> bool:
        return self.__has_diff


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
        self.expected_diff_size = expected_diff_size
        self.actual_diff_size = actual_diff_size
        self.expected_diff_percent = Decimal(str(expected_diff_percent))
        self.actual_diff_percent = actual_diff_percent
        self.diff_table = []
        self._build_diff_table()

    def get_diff_table(self) -> str:
        return "".join(self.diff_table)

    def _build_diff_table(self):
        self.__append_separator()
        self.__append_row("", "Expected", "Actual")
        self.__append_separator()
        self.__append_row(
            "diff_size", str(self.expected_diff_size), str(self.actual_diff_size)
        )
        self.__append_row(
            "diff_percent",
            str(self.expected_diff_percent),
            f"{self.actual_diff_percent:.3f}",
        )
        self.__append_separator()

    def __append_separator(self):
        self.diff_table.append(self.__separator_tpl)

    def __append_row(self, label: str, expected: str, actual: str):
        self.diff_table.append(self.__row_tpl.format(label, expected, actual))
