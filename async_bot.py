import os

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType, MediaGroup
from aiogram.utils import executor
from dotenv import load_dotenv

from file_managers import clean_photo_directory, save_img
from image_processing import create_watermark

# check if media_group_id for catching messages before /start
flag_group_id = None

storage = MemoryStorage()

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot_token = os.getenv('TOKEN')
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage)


class UserData(StatesGroup):
    watermark = State()
    image = State()
    watermarked = State()


@dp.message_handler(commands=['start', 'help'])
async def start_process(message: types.Message):
    chat_id = message.from_user.id

    await bot.send_message(
        chat_id, 'Hi.\n\nI receive a forwarded or '
        'a direct message with images (and text if you want to), '
        'put a watermark on them, and send you the message back.\n\n'
        '/set_watermark to start. You can change a watermark '
        'later with the same command.')


@dp.message_handler(commands=['set_watermark'], state='*')
async def set_watermark(message: types.Message):
    await UserData.watermark.set()
    await bot.send_message(message.from_user.id,
                           'Send a watermark in png format. '
                           'Load it as a document.')


@dp.message_handler(lambda message: not message.document,
                    state=UserData.watermark)
async def process_watermark_invalid(message: types.Message):
    return await message.reply("Please, try again. "
                               "I was not a png document.")


@dp.message_handler(content_types=ContentType.DOCUMENT,
                    state=UserData.watermark)
async def process_watermark(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id

    async with state.proxy() as data:
        data['chat_id'] = chat_id
        if 'watermark' in data:
            clean_photo_directory(data['watermark'])
        data['watermark'] = await save_img(
            message.document.file_id, bot)

    await UserData.next()
    await bot.send_message(chat_id,
                           "Forward/send a message with images, "
                           "on which you want to put a watermark.")


@dp.message_handler(lambda message: not message.photo,
                    state=UserData.image)
async def process_media_group_invalid(message: types.Message):
    return await message.reply(
        "Please, try again. The message doesn`t contain images.")


@dp.message_handler(content_types=ContentType.PHOTO,
                    state=UserData.image)
async def process_media_group(message: types.Message, state: FSMContext):
    if 'photo' not in await state.get_data():
        await state.update_data(photo=[message.photo[-1].file_id])
        await state.update_data(message=[message.caption])
        await bot.send_message(message.chat.id,
                               "Type any word to continue...")
        await UserData.next()
    else:
        async with state.proxy() as data:
            data['photo'].append(message.photo[-1].file_id)
            data['message'].append(message.caption)


@dp.message_handler(state=UserData.watermarked)
async def put_watermark(message, state: FSMContext):
    # getting photos, captions from state
    data = await state.get_data()
    photos = data['photo']
    text = data['message']
    watermark = data['watermark']

    # creating watermarks
    watermarked_img = []
    for photo in photos:
        file_info = await bot.get_file(photo)
        img = await bot.download_file(file_info.file_path)
        watermarked_img.append(await create_watermark(img, watermark))

    # creating MediaGroup
    media = MediaGroup()
    for photo, cap in zip(watermarked_img, text):
        if isinstance(cap, str):
            media.attach_photo(types.InputFile(photo), cap)
        else:
            media.attach_photo(types.InputFile(photo))

    await bot.send_media_group(message.from_user.id, media)

    await bot.send_message(message.from_user.id,
                           "Your message is ready.\n\n"
                           "Forward/send a message with images, "
                           "if you want to put the watermark again.\n\n"
                           "If you want to change the watermark, "
                           "/set_watermark again.")

    await state.set_state(UserData.image.state)
    async with state.proxy() as data:
        del data['photo']


@dp.message_handler(content_types=ContentType.all())
async def catch_messages_before_start(message: types.Message):
    global flag_group_id
    if message.media_group_id and not flag_group_id:
        flag_group_id = message.media_group_id
        await bot.send_message(
            message.from_user.id, 'To start, text /start or /help')
    else:
        if not message.media_group_id:
            flag_group_id = None
            await bot.send_message(
                message.from_user.id, 'To start, text /start or /help')


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,
                           on_shutdown=shutdown)
