from PIL import Image

from src.util.allure.allure_util import AllureUtil
from src.util.screenshot import image_util
from src.util.screenshot.screen_diff_table import DiffTable, DiffTableRow

_MAX_PERCENT_OF_TOLERANCE = 0.2
_MIN_RATIO_DIFF = 1.0 - _MAX_PERCENT_OF_TOLERANCE
_MAX_RATIO_DIFF = 1.0 + _MAX_PERCENT_OF_TOLERANCE


class ScreenDiffResult:

    def __init__(
        self,
        expected: Image.Image,
        actual: Image.Image,
        percent_of_tolerance: float = 0.0,
    ):
        if not (0.0 <= percent_of_tolerance <= _MAX_PERCENT_OF_TOLERANCE):
            raise ValueError(
                f"Illegal percent of tolerance value. "
                f"Allowed between [0, {_MAX_PERCENT_OF_TOLERANCE}]"
            )

        self.__expected = expected
        self.__actual = actual
        self.__percent_of_tolerance = percent_of_tolerance
        self.__has_diff = self.__calculate_diff()

    @property
    def has_diff(self) -> bool:
        return self.__has_diff

    def __calculate_diff(self) -> bool:
        expected_image_pixels = self.__expected.width * self.__expected.height
        actual_image_pixels = self.__actual.width * self.__actual.height
        n_exp_img, n_act_img = image_util.normalize_images(
            self.__expected, self.__actual
        )
        diff_image = image_util.get_diff_image(n_exp_img, n_act_img)
        self.__colored_diff_image = image_util.colored_diff_image(n_exp_img, diff_image)

        self.__expected_diff_size = int(
            round(expected_image_pixels * self.__percent_of_tolerance)
        )
        self.__actual_diff_size = image_util.calculate_diff_pixels(diff_image)
        self.__actual_diff_percent = self.__actual_diff_size / expected_image_pixels
        size_ratio = expected_image_pixels / actual_image_pixels
        invalid_resolution = (
            size_ratio < _MIN_RATIO_DIFF or size_ratio > _MAX_RATIO_DIFF
        )
        has_diff = self.__actual_diff_size > self.__expected_diff_size

        self.__diff_table = DiffTable(
            [
                DiffTableRow(
                    "diff_size",
                    self.__expected_diff_size,
                    self.__actual_diff_size,
                ),
                DiffTableRow(
                    "diff_percent",
                    self.__percent_of_tolerance,
                    f"{self.__actual_diff_percent:.3f}",
                ),
            ]
        ).diff_table

        return invalid_resolution or has_diff

    def attach_diff_to_allure(self):
        AllureUtil.attach_screen_diff(
            self.__expected, self.__actual, self.__colored_diff_image
        )
        AllureUtil.attach_screen_diff_table(self.__diff_table)
