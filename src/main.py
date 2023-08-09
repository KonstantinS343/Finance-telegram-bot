import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from aioredis import Redis

from config import TELEGRAM


logging.basicConfig(level=logging.INFO)

redis = Redis(host='localhost', port='6379', db='3')

memory = MemoryStorage()
bot = Bot(token=TELEGRAM, parse_mode='html')
dp = Dispatcher(bot, storage=memory)

from telegram.telegram_api import *

if __name__ == '__main__':
    executor.start_polling(dp)
