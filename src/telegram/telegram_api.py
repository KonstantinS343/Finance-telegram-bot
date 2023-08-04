import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram.buttons import BUTTON_MANAGE_MONEY, BUTTON_CANCEL
from main import dp, bot
from telegram.utils import UserInput


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAIxgmR_WduWkzBmN4xogt4TSPMCiukoAAI2FgACcmugS6XaTV2HP2QpLwQ')
    await message.answer('<b>Привет!</b> 👋'
                         '\n '
                         '\n'
                         'Я рад приветствовать тебя в нашем телеграмм боте по учету финансов 💸 \n'
                         '\n'
                         'Я здесь, чтобы помочь тебе контролировать свои финансы🤑, планировать бюджет и достигать финансовых целей 📈.'
                         'С моей помощью ты сможешь вести учет доходов и расходов, анализировать свои финансовые показатели.'
                         '\n '
                         '\n'
                         '<b>Будем работать вместе!</b> 😁', reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(lambda message: message.text == 'Доход')
async def income_handler(message: types.Message):
    logging.info('INCOME')
    await UserInput.input.set()
    await message.answer('ДОХОД:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите ваш доход', reply_markup=BUTTON_CANCEL)


@dp.message_handler(state=UserInput.input)
async def input_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text)
    await state.finish()


@dp.message_handler(lambda message: message.text == 'Расход')
async def expenditure_handler(message: types.Message):
    logging.info('EXPENDITURE')
    await UserInput.input.set()
    await message.answer('РАСХОД:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите ваш расход', reply_markup=BUTTON_CANCEL)


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
