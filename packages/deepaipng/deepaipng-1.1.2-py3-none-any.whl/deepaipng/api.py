import os
import uuid
from typing import Optional, Tuple

import httpx
from dotenv import load_dotenv
from PIL import Image


def is_valid_uuid_v4(api_key: str) -> bool:
    """
    Check if the given string is a valid UUID version 4.

    Args:
        api_key (str): API key to check.

    Returns:
        bool: True if the API key is a valid UUID version 4, otherwise False.

        Author:
        dj@deepai.org
    """
    try:
        return uuid.UUID(api_key).version == 4
    except ValueError:
        return False


def raise_for_apikey(api_key: Optional[str] = None) -> str:
    """
    Validates and retrieves the DeepAI API key, ensuring it is a valid UUID version 4.

    Args:
        api_key (str | None): Optionally provided API key.

    Returns:
        str: Valid API key.

    Raises:
        ValueError: If no API key is provided, found, or if the API key is not a valid UUID version 4.

    Author:
        dj@deepai.org
    """
    if api_key:
        if not is_valid_uuid_v4(api_key):
            raise ValueError("The provided API key is not a valid UUID version 4.")
        return api_key
    load_dotenv()
    api_key = os.getenv("DEEPAI_API_KEY")
    if not api_key:
        raise ValueError("The DeepAI API key was not found.")
    if not is_valid_uuid_v4(api_key):
        raise ValueError("The API key is not a valid UUID version 4.")
    return api_key


def resize_and_center_crop(img_path: str, target_size: int) -> Image.Image:
    """
    Resize and crop an image to fit a square of target_size while maintaining aspect ratio.

    Args:
        img_path (str): Path to the input image.
        target_size (int): The target size for the image's width and height in pixels.

    Returns:
        Image.Image: The resized and cropped image.

    Raises:
        ValueError: If an API key is not provided or found

    Author:
        dj@deepai.org
    """
    with Image.open(img_path) as img:
        img = img.convert("RGBA")
        img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
        new_img = Image.new("RGBA", (target_size, target_size), (255, 255, 255, 0))
        left = (target_size - img.width) // 2
        top = (target_size - img.height) // 2
        new_img.paste(img, (left, top))
        return new_img


def remove_background(img_path: str, api_key: Optional[str] = None) -> bytes:
    """
    Remove the background of an image using DeepAI's Background Remover API.

    Args:
        img_path (str): Path to the image file.
        api_key (str): DeepAI API key.

    Returns:
        bytes: The image data with a transparent background.

    Raises:
        httpx.HTTPError: If the API request fails.

    Author:
        dj@deepai.org
    """
    api_key = raise_for_apikey(api_key)
    with open(img_path, "rb") as file:
        response = httpx.post(
            "https://api.deepai.org/api/background-remover",
            files={"image": file},
            headers={"api-key": api_key},
            timeout=30,
        )
    response.raise_for_status()
    result_url = response.json()["output_url"]
    return httpx.get(result_url).content


def process_image(args: Tuple[str, str, int], api_key: Optional[str] = None) -> None:
    """
    Process the image: resize, crop, remove background.

    Args:
        args (Tuple[str, str, int]): Tuple containing input_path, output_path, and target_size.

    Author:
        dj@deepai.org
    """
    input_path, output_path, target_size = args
    try:
        resized_img = resize_and_center_crop(input_path, target_size)
        resized_img.save(".tmp.png")
        transparent_img_bytes = remove_background(
            ".tmp.png", api_key=raise_for_apikey(api_key)
        )
        with open(output_path, "wb") as out_file:
            out_file.write(transparent_img_bytes)
        print("Image processed and saved to", output_path)
    except Exception as e:
        print("Failed to process image:", str(e))
    finally:
        if os.path.exists(".tmp.png"):
            os.remove(".tmp.png")
