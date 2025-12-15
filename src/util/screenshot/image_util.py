import base64
import io
import os

from PIL import Image, ImageChops, ImageOps

from src.util import system_util


def create_blank_image(absolute_path: str, from_image: Image.Image) -> None:
    """
    Create new image with white background, matching the mode and size of from_image.
    :param absolute_path: (str) absolute path to new image
    :param from_image: (PIL.Image.Image)
    """
    # Изменение: Всегда используем "white" — Pillow адаптирует под mode (для RGBA — с альфа=255)
    # Image.new(
    #     mode=from_image.mode,
    #     size=from_image.size,
    #     color="white",
    # ).save(
    #     absolute_path, format="PNG"
    # )
    Image.new(mode=from_image.mode,size=from_image.size, color="white").save(absolute_path)



def crop_image(byte_image: bytes, location: dict, size: dict) -> Image.Image:
    """Crop an image from the byte image"""
    image_file = Image.open(io.BytesIO(byte_image))
    return image_file.crop(
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


def get_diff_image(
    expected_screenshot: Image.Image, actual_screenshot: Image.Image
) -> Image.Image:
    """Make diff image from expected and actual screenshot"""
    diff = ImageChops.difference(expected_screenshot, actual_screenshot)
    grayscale_diff = ImageOps.grayscale(diff)
    mask = Image.eval(grayscale_diff, lambda x: 255 if x > 0 else 0)

    mode = expected_screenshot.mode
    color = (255, 0, 0) if mode == "RGB" else (255, 0, 0, 255)

    red_layer = Image.new(mode, expected_screenshot.size, color)
    return Image.composite(red_layer, expected_screenshot, mask)
