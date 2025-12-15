import io

from PIL import Image
from selene import browser, Element
import time

from selene.support.conditions.be import visible

from src.util.image_util import crop_image


def take_element_screenshot(element: Element, hover:bool, timeout:float) -> Image:

    element.should(visible)

    web_element = element()
    location = web_element.location_once_scrolled_into_view
    size = web_element.size
    # location, size = transform_coordinates(driver, location, size)

    if hover:
        element.hover()
    if timeout > 0:
        time.sleep(timeout)

    return crop_image(
        byte_image=browser.driver.get_screenshot_as_png(),
        location=location,
        size=size,
    )


def __transform_coordinates(driver, location, size):
    dpr = driver.execute_script("return window.devicePixelRatio;") or 1
    location = {
        "x": int(location["x"] * dpr),
        "y": int(location["y"] * dpr),
    }
    size = {
        "width": int(size["width"]) * dpr,
        "height": int(size["height"]) * dpr
    }
    return location, size