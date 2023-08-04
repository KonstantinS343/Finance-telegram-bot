import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import TELEGRAM


logging.basicConfig(level=logging.INFO)

memory = MemoryStorage()
bot = Bot(token=TELEGRAM, parse_mode='html')
dp = Dispatcher(bot, storage=memory)

from telegram.telegram_api import *

if __name__ == '__main__':
    executor.start_polling(dp)
