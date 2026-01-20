import io
import os
import time

from PIL import Image
from selene import browser, Element
from selenium.webdriver.remote.webdriver import WebDriver

from src.config.config import CFG
from src.util import system_util
from src.util.screenshot import image_util
from src.util.screenshot.screen_diff import ScreenDiffResult


def take_element_screenshot(
    element: Element, hover: bool, timeout: float
) -> Image.Image:

    web_element = element()
    location = web_element.location_once_scrolled_into_view

    if hover:
        element.hover()
    if timeout > 0:
        time.sleep(timeout)

    size = web_element.size
    location, size = __transform_coordinates(browser.driver, location, size)

    bytes_image = io.BytesIO(browser.driver.get_screenshot_as_png())
    image = Image.open(bytes_image)

    return image_util.crop_image(
        image=image,
        location=location,
        size=size,
    )


def compare_and_save_screenshot(
    actual_screenshot: Image.Image,
    path_to_screenshot: str,
    percent_of_tolerance: float = 0,
    rewrite_screenshot: bool = False,
    component_name: str = "Component",
) -> None:

    abs_path = system_util.get_path_in_resources(path_to_screenshot)
    expected_not_exists = not os.path.exists(abs_path)

    if expected_not_exists:
        image_util.create_blank_image(abs_path, actual_screenshot.size)

    expected_screenshot = Image.open(abs_path, formats=["PNG"])
    screen_diff = ScreenDiffResult(
        expected=expected_screenshot,
        actual=actual_screenshot,
        percent_of_tolerance=percent_of_tolerance,
    )

    if expected_not_exists or CFG.rewrite_all_screenshots or rewrite_screenshot:
        actual_screenshot.save(abs_path, save_all=True)

    screen_diff.attach_diff_to_allure()

    if screen_diff.has_diff and not CFG.rewrite_all_screenshots:
        raise AssertionError(f"{component_name} screenshot mismatch")


def __transform_coordinates(
    driver: WebDriver,
    location: dict[str, int],
    size: dict[str, int],
) -> tuple[dict[str, int], dict[str, int]]:
    dpr: float = float(driver.execute_script("return window.devicePixelRatio;") or 1)
    location = {
        "x": int(int(location["x"] * dpr)),
        "y": int(int(location["y"] * dpr)),
    }
    size = {
        "width": int(int(size["width"]) * dpr),
        "height": int(int(size["height"]) * dpr),
    }
    return location, size
