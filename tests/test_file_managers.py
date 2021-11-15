import io

from file_managers import clean_photo_directory
import tempfile

from PIL import Image
from image_processing import turn_into_io_base


def test_clean_photo_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        assert clean_photo_directory('non_existing.png', tmp_dir) is None


def test_image():
    img = Image.new('RGB', (100, 100))
    turned_img = turn_into_io_base(img)
    assert isinstance(turned_img, io.BytesIO)
