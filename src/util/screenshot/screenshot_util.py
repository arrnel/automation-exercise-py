import os
import time

from PIL import Image
from selene import browser, Element
from selene.support.conditions.be import visible
from selenium.webdriver.remote.webdriver import WebDriver

from src.config.config import CFG
from src.util.screenshot.image_util import crop_image, create_blank_image
from src.util.screenshot.screen_diff import ScreenDiffResult
from src.util.system_util import get_path_in_resources


def take_element_screenshot(element: Element, hover: bool, timeout: float) -> Image:
    element.should(visible)

    web_element = element()
    location = web_element.location_once_scrolled_into_view
    size = web_element.size
    location, size = __transform_coordinates(browser.driver, location, size)

    if hover:
        element.hover()
    if timeout > 0:
        time.sleep(timeout)

    return crop_image(
        byte_image=browser.driver.get_screenshot_as_png(),
        location=location,
        size=size,
    )


def compare_and_save_screenshot(
        actual_screenshot: Image,
        path_to_screenshot: str,
        percent_of_tolerance: float = 0,
        rewrite_screenshot: bool = False,
        component_name: str = "Component",
) -> None:
    abs_path = get_path_in_resources(path_to_screenshot)
    expected_exists = os.path.exists(abs_path)

    if not expected_exists:
        create_blank_image(abs_path, actual_screenshot)

    expected_screenshot = Image.open(abs_path, formats=["PNG"])
    screen_diff = ScreenDiffResult(
        expected=expected_screenshot,
        actual=actual_screenshot,
        percent_of_tolerance=percent_of_tolerance,
    )

    if not expected_exists or CFG.rewrite_all_screenshots or (rewrite_screenshot and screen_diff.has_diff):
        actual_screenshot.save(abs_path, save_all=True)

    screen_diff.attach_diff_to_allure()

    if screen_diff.has_diff:
        raise AssertionError(f"{component_name} screenshot mismatch")


def __transform_coordinates(
        driver: WebDriver,
        location: dict[str, int],
        size: dict[str, int]
) -> tuple[dict[str, int], dict[str, int]]:
    dpr: float = float(driver.execute_script("return window.devicePixelRatio;") or 1)
    location = {
        "x": int(int(location["x"] * dpr)),
        "y": int(int(location["y"] * dpr)),
    }
    size = {
        "width": int(int(size["width"]) * dpr),
        "height": int(int(size["height"]) * dpr)
    }
    return location, size
