import base64
import io
from pathlib import Path
from typing import Tuple

import numpy as np
from PIL import Image, ImageChops, ImageOps

_RGB_MODE = "RGB"


def create_blank_image(absolute_path: str, size: Tuple[int, int]) -> None:
    """
    Create new PNG RGB image with white background.

    Args:
        :param absolute_path: (str) absolute path to new image
        :param size: (Tuple[int, int]) size of new image
    """
    output_path = Path(absolute_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.new(
        mode=_RGB_MODE,
        size=size,
        color="white",
    ).save(absolute_path, format="PNG")


def crop_image(image: Image.Image, location: dict, size: dict) -> Image.Image:
    """Crop an image from the byte image"""
    return image.crop(
        (
            float(location["x"]),
            float(location["y"]),
            float(location["x"]) + float(size["width"]),
            float(location["y"]) + float(size["height"]),
        )
    )


def get_img_base64(img: Image.Image, image_format: str = "PNG") -> str:
    """Get the base64 encoded image bytes"""
    buf = io.BytesIO()
    img.save(buf, format=image_format)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def calculate_diff_pixels(image: Image.Image) -> int:
    diff_array = np.array(image)
    if len(diff_array.shape) == 3:  # Для многоканальных изображений
        actual_diff_size = np.count_nonzero(np.any(diff_array != 0, axis=-1))
    else:
        actual_diff_size = np.count_nonzero(diff_array)
    return int(actual_diff_size)


def get_diff_image(
    expected_screenshot: Image.Image, actual_screenshot: Image.Image
) -> Image.Image:
    """Make diff image from expected and actual screenshot"""
    diff = ImageChops.difference(expected_screenshot, actual_screenshot)
    return ImageOps.grayscale(diff).convert(_RGB_MODE)


def normalize_images(
    img1: Image.Image,
    img2: Image.Image,
    background_color: str = "white",
) -> tuple[Image.Image, Image.Image]:
    """
    Converts two images to the same mode and size.
    If the sizes are different, they are placed on the maximum-sized canvases.
    """

    img1 = convert_to_rgb(img1)
    img2 = convert_to_rgb(img2)

    if img1.size == img2.size:
        return img1, img2

    max_width = max(img1.width, img2.width)
    max_height = max(img1.height, img2.height)

    canvas1 = Image.new(_RGB_MODE, (max_width, max_height), background_color)
    canvas2 = Image.new(_RGB_MODE, (max_width, max_height), background_color)

    origin = (0, 0)
    canvas1.paste(img1, origin)
    canvas2.paste(img2, origin)

    return canvas1, canvas2


def convert_to_rgb(img: Image.Image) -> Image.Image:
    if img.mode == _RGB_MODE:
        return img
    return img.convert(_RGB_MODE)


def colored_diff_image(expected_image: Image.Image, diff: Image.Image) -> Image.Image:
    """Make colored image from expected and diff image"""
    grayscale_diff = ImageOps.grayscale(diff)
    mask = Image.eval(grayscale_diff, lambda x: 255 if x > 0 else 0)

    red_layer = Image.new(_RGB_MODE, expected_image.size, "red")
    return Image.composite(red_layer, expected_image, mask)
