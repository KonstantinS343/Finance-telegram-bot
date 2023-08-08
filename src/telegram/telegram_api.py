import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram.buttons import BUTTON_MANAGE_MONEY, BUTTON_CANCEL
from main import dp, bot
from telegram.utils import UserInput
from .messages import START_MESSAGE
from middleware.service import (
    _add_new_user,
    _add_new_category,
    _show_all_categories,
    _get_balance,
    _add_income,
    _add_expenditure)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await _add_new_user(message.from_user.username)
    await bot.send_sticker(message.from_user.id, sticker='CAACAgIAAxkBAAIxgmR_WduWkzBmN4xogt4TSPMCiukoAAI2FgACcmugS6XaTV2HP2QpLwQ')
    await message.answer(START_MESSAGE, reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(lambda message: message.text == 'Доход')
async def income_handler(message: types.Message):
    logging.info('INCOME')
    await UserInput.income_input.set()
    await message.answer('ДОХОД:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите ваш доход', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Расход')
async def expenditure_handler(message: types.Message):
    logging.info('EXPENDITURE')
    await UserInput.expenditure_input.set()
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


@dp.message_handler(lambda message: message.text == 'Категории')
async def categories_show_handler(message: types.Message):
    logging.info('CATEGORIES')
    await message.answer('Вот список текущих категорий:')
    all_categories = await _show_all_categories(message.from_user.username)

    telegram_formatted_categories = ('\n').join(category.name.capitalize() for category in all_categories)
    await message.answer(telegram_formatted_categories, reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(lambda message: message.text == 'Добавить категорию')
async def categories_show_handler(message: types.Message):
    logging.info('ADD CATEGORIES')
    await UserInput.add_categories_input.set()
    await message.answer('НОВАЯ КАТЕГОРИЯ:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите название новой категории', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Удалить категорию')
async def categories_show_handler(message: types.Message):
    logging.info('DELETE CATEGORIES')
    await UserInput.delete_categories_input.set()
    await message.answer('УДАЛЕНИЕ КАТЕГОРИИ:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите название категории', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Баланс')
async def balance_show_handler(message: types.Message):
    logging.info('BALANCE')
    await message.answer('ВАШ ТЕКУЩИЙ БАЛАНС:')

    user_balance = await _get_balance(message.from_user.username)

    await message.answer(user_balance[0].balance, reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(state=UserInput.income_input)
async def income_input_handler(message: types.Message, state: FSMContext):
    quantity, category = message.text.split()
    await _add_income(
        username=message.from_user.username,
        quantity=float(quantity),
        category=category.lower()
    )
    await message.answer(text='Новая запись:')
    await message.answer(text=f'ДОХОД {message.text}', reply_markup=BUTTON_MANAGE_MONEY)
    await state.finish()


@dp.message_handler(state=UserInput.expenditure_input)
async def expenditure_input_handler(message: types.Message, state: FSMContext):
    quantity, category = message.text.split()
    await _add_expenditure(
        username=message.from_user.username,
        quantity=float(quantity),
        category=category.lower()
    )
    await message.answer(text='Новая запись:')
    await message.answer(text=f'РАСХОД {message.text}', reply_markup=BUTTON_MANAGE_MONEY)
    await state.finish()


@dp.message_handler(state=UserInput.add_categories_input)
async def add_categories_input_handler(message: types.Message, state: FSMContext):
    await _add_new_category(category_name=message.text.lower(), username=message.from_user.username)
    await message.answer('Категория успешно добавлена!', reply_markup=BUTTON_MANAGE_MONEY)
    await state.finish()


@dp.message_handler(state=UserInput.delete_categories_input)
async def delete_categories_input_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text)
    await state.finish()
