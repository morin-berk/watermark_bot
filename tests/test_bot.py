import os

import pytest
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from async_bot import catch_messages_before_start

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot_token = os.getenv('TOKEN')

pytestmark = pytest.mark.asyncio


@pytest.fixture(name='bot')
async def bot_fixture():
    """ Bot fixture """
    _bot = Bot(token=bot_token)
    yield _bot
    await _bot.close()


