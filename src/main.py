import logging
from pathlib import Path

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.utils import executor

from config import TELEGRAM, DEBUG
from i18n import setup_middleware


if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


memory = MemoryStorage()
bot = Bot(token=TELEGRAM)
dp = Dispatcher(bot, storage=memory)


dp.middleware.setup(LoggingMiddleware())
i18n = setup_middleware(dp=dp)

_ = i18n.gettext


from telegram.category_handlers import *
from telegram.common_handlers import *
from telegram.language_handlers import *
from telegram.main_handlers import *
from telegram.report_handlers import *

if __name__ == '__main__':
    executor.start_polling(dp)
