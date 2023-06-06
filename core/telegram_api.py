import logging
import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from aiogram.utils import executor

from core.buttons import BUTTON_MANAGE_MONEY, BUTTON_CANCEL

load_dotenv(os.path.dirname(__file__) + '/config/.env')
logging.basicConfig(level=logging.INFO)

memory = MemoryStorage()
bot=Bot(token=os.getenv('TELEGRAM'), parse_mode='html')
dp = Dispatcher(bot, storage=memory)

class UserInput(StatesGroup):
    input = State()

def launch():
    executor.start_polling(dp)
    
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAIxgmR_WduWkzBmN4xogt4TSPMCiukoAAI2FgACcmugS6XaTV2HP2QpLwQ')
    await message.answer('<b>Привет!</b> 👋' \
                        '\n '\
                        '\n'\
                        'Я рад приветствовать тебя в нашем телеграмм боте по учету финансов 💸\n' \
                        '\n'\
                        'Я здесь, чтобы помочь тебе контролировать свои финансы🤑, планировать бюджет и достигать финансовых целей 📈. '\
                        'С моей помощью ты сможешь вести учет доходов и расходов, анализировать свои финансовые показатели.' \
                        '\n '\
                        '\n'\
                        '<b>Будем работать вместе!</b> 😁', reply_markup=BUTTON_MANAGE_MONEY)

@dp.callback_query_handler(text='income')
async def start_bot(callback_query: types.CallbackQuery):
    await UserInput.input.set()
    await callback_query.message.answer('Введите ваш доход', reply_markup=BUTTON_CANCEL)
    await callback_query.answer()
    
@dp.message_handler(state=UserInput.input)
async def input_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text)
    await state.finish()
    
@dp.callback_query_handler(text='expenditure')
async def start_bot(callback_query: types.CallbackQuery):
    await UserInput.input.set()
    await callback_query.message.answer('Введите ваш расход', reply_markup=BUTTON_CANCEL)
    await callback_query.answer()
    
@dp.callback_query_handler(state='*', text='cancel')
async def cancel_input(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await callback_query.answer()
        return
    
    logging.info(f'CANCEL, CURRENT STATE: {current_state}')
    await state.finish()
    await callback_query.message.answer('Отменено', reply_markup=BUTTON_MANAGE_MONEY)
    await callback_query.answer()
