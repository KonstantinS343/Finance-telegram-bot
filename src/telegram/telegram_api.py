import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram.buttons import BUTTON_MANAGE_MONEY, BUTTON_CANCEL
from main import dp, bot
from telegram.utils import UserInput
from .messages import (
    START_MESSAGE,
    TELEGRAM_USERNAME_EXISTANCE_MESSAGE,
    USER_INPUT_RULE,
    FLOAT_NUMBER_ERROR
)
from middleware.user import _add_new_user
from middleware.accounting import (
    _add_new_category,
    _show_all_categories,
    _get_balance,
    _add_income,
    _add_expenditure,
    _delete_category
)
from middleware.general_handlers import (
    check_telegram_username,
    check_user_existence,
    validate_income_and_expenditure,
    category_does_not_exist,
    category_already_exist
)
from exception import (
    UserAlreadyExists,
    UserNameNotDefined,
    UnsupportedInput,
    CategoryDoesNotExist,
    CategoryAlreadyExist
)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    try:
        await check_telegram_username(message.from_user.username)
        await check_user_existence(message.from_user.username)
    except UserNameNotDefined:
        await message.answer(TELEGRAM_USERNAME_EXISTANCE_MESSAGE, reply_markup=BUTTON_MANAGE_MONEY)
    except UserAlreadyExists:
        await message.answer(START_MESSAGE, reply_markup=BUTTON_MANAGE_MONEY)
    else:
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
    all_categories = await _show_all_categories(message.from_user.username)

    await message.answer('Вот список текущих категорий:\n' + all_categories, reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(lambda message: message.text == 'Добавить категорию')
async def categories_show_handler(message: types.Message):
    logging.info('ADD CATEGORIES')
    await UserInput.add_categories_input.set()
    await message.answer('НОВАЯ КАТЕГОРИЯ:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Введите название новой категории', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Удалить категорию')
async def categories_delete_handler(message: types.Message):
    logging.info('DELETE CATEGORIES')
    await UserInput.delete_categories_input.set()
    await message.answer('УДАЛЕНИЕ КАТЕГОРИИ:', reply_markup=types.ReplyKeyboardRemove())
    all_categories = await _show_all_categories(message.from_user.username)

    await message.answer('Мои категории:' + all_categories)
    await message.answer('Введите название категории', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Баланс')
async def balance_show_handler(message: types.Message):
    logging.info('BALANCE')
    await message.answer('ВАШ ТЕКУЩИЙ БАЛАНС:')

    user_balance = await _get_balance(message.from_user.username)

    await message.answer(round(user_balance, 2), reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(state=UserInput.income_input)
async def income_input_handler(message: types.Message, state: FSMContext):
    try:
        await validate_income_and_expenditure(message.text, message.from_user.username)
    except UnsupportedInput:
        await message.answer(USER_INPUT_RULE, reply_markup=BUTTON_MANAGE_MONEY)
    except ValueError:
        await message.answer(FLOAT_NUMBER_ERROR, reply_markup=BUTTON_MANAGE_MONEY)
    else:
        quantity, category = message.text.split()
        await _add_income(
            username=message.from_user.username,
            quantity=float(quantity),
            category=category.lower()
        )
        await message.answer('Новая запись:')
        await message.answer(f'ДОХОД {message.text}', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.finish()


@dp.message_handler(state=UserInput.expenditure_input)
async def expenditure_input_handler(message: types.Message, state: FSMContext):
    try:
        await validate_income_and_expenditure(message.text, message.from_user.username)
    except UnsupportedInput:
        await message.answer(USER_INPUT_RULE, reply_markup=BUTTON_MANAGE_MONEY)
    except ValueError:
        await message.answer(FLOAT_NUMBER_ERROR, reply_markup=BUTTON_MANAGE_MONEY)
    else:
        quantity, category = message.text.split()
        await _add_expenditure(
            username=message.from_user.username,
            quantity=float(quantity),
            category=category.lower()
        )
        await message.answer('Новая запись:')
        await message.answer(f'РАСХОД {message.text}', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.finish()


@dp.message_handler(state=UserInput.add_categories_input)
async def add_categories_input_handler(message: types.Message, state: FSMContext):
    try:
        await category_already_exist(message.text)
    except CategoryAlreadyExist:
        await message.answer('Посмотрите внимательно, кажется такая категория уже существует!', reply_markup=BUTTON_MANAGE_MONEY)
    else:
        await _add_new_category(category_name=message.text.lower(), username=message.from_user.username)
        await message.answer('Категория успешно добавлена!', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.finish()


@dp.message_handler(state=UserInput.delete_categories_input)
async def delete_categories_input_handler(message: types.Message, state: FSMContext):
    try:
        await category_does_not_exist(message.text)
    except CategoryDoesNotExist:
        await message.answer('Мне кажется или такой категории нет?', reply_markup=BUTTON_MANAGE_MONEY)
    else:
        await _delete_category(username=message.from_user.username, category=message.text.lower())
        await message.answer('Категория успешно удалена!', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.finish()
