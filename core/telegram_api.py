import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.utils import executor

load_dotenv(os.path.dirname(__file__) + '/config/.env')
logging.basicConfig(level=logging.INFO)

bot=Bot(token=os.getenv('TELEGRAM'), parse_mode='html')
dp = Dispatcher(bot)

def launch():
    executor.start_polling(dp)
    
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.answer('Hello')