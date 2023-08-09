import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

from redis.asyncio import Redis

from config import TELEGRAM, REDIS_HOST, REDIS_PORT


logging.basicConfig(level=logging.INFO)

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db='3')

memory = MemoryStorage()
bot = Bot(token=TELEGRAM, parse_mode='html')
dp = Dispatcher(bot, storage=memory)

dp.middleware.setup(LoggingMiddleware())

from telegram.telegram_api import *

if __name__ == '__main__':
    executor.start_polling(dp)
