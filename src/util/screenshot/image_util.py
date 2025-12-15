import base64
import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageOps


def create_blank_image(absolute_path: str, from_image: Image.Image) -> None:
    """
    Create new image with white background, matching the mode and size of from_image.
    :param absolute_path: (str) absolute path to new image
    :param from_image: (PIL.Image.Image)
    """
    output_path = Path(absolute_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.new(
        mode=from_image.mode,
        size=from_image.size,
        color="white",
    ).save(
        absolute_path, format="PNG"
    )


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
    ).convert("RGB")


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
    return ImageOps.grayscale(diff)


def normalize_images(
        img1: Image.Image,
        img2: Image.Image,
        background_color: str = "white",
) -> tuple[Image.Image, Image.Image]:
    """
    Converts two images to the same mode and size.
    If the sizes are different, they are placed on the maximum-sized canvases.
    """

    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    if img1.size == img2.size:
        return img1, img2

    max_width = max(img1.width, img2.width)
    max_height = max(img1.height, img2.height)

    canvas1 = Image.new("RGB", (max_width, max_height), background_color)
    canvas2 = Image.new("RGB", (max_width, max_height), background_color)

    canvas1.paste(img1, (0, 0))
    canvas2.paste(img2, (0, 0))

    return canvas1, canvas2


def colored_diff_image(expected_image: Image.Image, diff: Image.Image) -> Image.Image:
    """Make colored image from expected and diff image"""
    grayscale_diff = ImageOps.grayscale(diff)
    mask = Image.eval(grayscale_diff, lambda x: 255 if x > 0 else 0)

    red_layer = Image.new("RGB", expected_image.size, "red")
    return Image.composite(red_layer, expected_image, mask)
