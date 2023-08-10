import logging
from pathlib import Path

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.utils import executor

from redis.asyncio import Redis

from config import TELEGRAM, REDIS_HOST, REDIS_PORT, DEBUG
from i18n import setup_middleware


if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db='3')

memory = MemoryStorage()
bot = Bot(token=TELEGRAM)
dp = Dispatcher(bot, storage=memory)


dp.middleware.setup(LoggingMiddleware())
i18n = setup_middleware(dp=dp)

_ = i18n.gettext


from telegram.telegram_api import *

if __name__ == '__main__':
    executor.start_polling(dp)
