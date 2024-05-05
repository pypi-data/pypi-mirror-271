import os
from argparse import ArgumentParser, Namespace
from typing import Tuple

from deepaipng.api import raise_for_apikey, remove_background, resize_and_center_crop


def parse_args() -> Tuple[str, str, int]:
    """
    Parse command line arguments for the image processing script.

        Author:
        dj@deepai.org
    """
    parser = ArgumentParser(
        description="Process images to fit specified dimensions with a transparent background."
    )
    parser.add_argument(
        "-i", "--input_path", type=str, help="Path to load the input image file."
    )
    parser.add_argument(
        "-o", "--output_path", type=str, help="Path to save the output image file."
    )
    parser.add_argument(
        "-s", "--size", type=int, default=120, help="Target size for the output image."
    )
    parser.add_argument(
        "-k",
        "--api-key",
        type=str,
        default="",
        help="DeepAI API key to use for the operation.",
    )
    args: Namespace = parser.parse_args()
    if args.api_key:
        os.environ["DEEPAI_API_KEY"] = raise_for_apikey(args.api_key)
    return args.input_path, args.output_path, args.size


def main() -> None:
    """
    Main function to handle image processing.
    """
    input_path, output_path, size = parse_args()
    api_key = raise_for_apikey()
    resized_img = resize_and_center_crop(input_path, size)
    resized_img.save("temp_image.png")
    transparent_img_bytes = remove_background("temp_image.png", api_key)
    with open(output_path, "wb") as out_file:
        out_file.write(transparent_img_bytes)
    print("Image processed and saved to", output_path)


if __name__ == "__main__":
    main()
