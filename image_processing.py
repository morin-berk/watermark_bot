"""Preprocess images with the pillow module, create watermarks."""
import io
from typing import Union
from PIL import Image


def turn_into_io_base(base_img: Image.Image) -> io.BytesIO:
    """Turns base_img into IOBase."""
    image_content = io.BytesIO()
    base_img.seek(0)
    base_img.save(image_content, format='JPEG')
    image_content.seek(0)
    return image_content


async def prepare_base_image(
        row_image: Union[io.BytesIO, io.FileIO]) -> Image.Image:
    """Transpose base img to prepare it for being watermarked."""
    base_image = Image.open(row_image)

    transparent = Image.new('RGBA',
                            (base_image.width, base_image.height),
                            (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    if transparent.mode != 'RGB':
        transparent = transparent.convert('RGB')
    return transparent


async def create_watermark(base_img: Union[io.BytesIO, io.FileIO],
                           watermark_image_path: str) -> io.BytesIO:
    """Takes prepared base_img, changes watermark size to 7% of
    a base_img.
    Place watermark to the right bottom corner of a base_img"""
    prep_base_img = await prepare_base_image(base_img)
    watermark = Image.open(watermark_image_path).convert('RGBA')

    x_size, y_size = (int(prep_base_img.width * 0.07),
                      int(prep_base_img.height * 0.07))
    watermark.thumbnail((x_size, y_size), Image.ANTIALIAS)

    # creating position, margin
    x, y = (int(prep_base_img.width * 0.1),
            int(prep_base_img.height * 0.1))
    position = prep_base_img.width - x, prep_base_img.height - y
    prep_base_img.paste(watermark, position, mask=watermark)

    return turn_into_io_base(prep_base_img)
