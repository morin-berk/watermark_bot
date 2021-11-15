"""Work with files and bot.message data."""
import os


async def get_file_info(file_id: str, bot):
    """Collects full file_info, file_name from telegram."""
    file_info = await bot.get_file(file_id)
    file_name, file_extension = os.path.splitext(file_info.file_path)
    return file_info, file_extension


async def save_img(file_id: str, bot) -> str:
    """Creates path for img, saves them.
    Returns src of the saved file."""
    file_info, file_extension = await get_file_info(file_id, bot)

    folder = os.path.join(os.getcwd(), 'photos\\')
    if not os.path.exists(folder):
        os.mkdir(folder)
    src = folder + file_id + file_extension

    await bot.download_file(file_info.file_path, src)

    return src


def clean_photo_directory(image: str, directory: str = None) -> None:
    """Cleans photo directory."""
    if not directory:
        directory = os.path.join(os.getcwd(), 'photos\\')
    if os.path.isdir(directory):
        try:
            os.remove(image)
        except FileNotFoundError:
            pass
