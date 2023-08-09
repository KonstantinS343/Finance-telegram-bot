from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram.buttons import BUTTON_MANAGE_MONEY, BUTTON_CANCEL
from main import dp, bot
from telegram.states import (
    IncomeState,
    ExpenditureState,
    AddCategoryState,
    DeleteCategoryState
)
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
        await check_telegram_username(username=message.from_user.username)
        await check_user_existence(username=message.from_user.username)
    except UserNameNotDefined:
        await message.answer(text=TELEGRAM_USERNAME_EXISTANCE_MESSAGE, reply_markup=BUTTON_MANAGE_MONEY)
    except UserAlreadyExists:
        await message.answer(text=START_MESSAGE, reply_markup=BUTTON_MANAGE_MONEY)
    else:
        await _add_new_user(username=message.from_user.username)
        await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAIxgmR_WduWkzBmN4xogt4TSPMCiukoAAI2FgACcmugS6XaTV2HP2QpLwQ')
        await message.answer(text=START_MESSAGE, reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(lambda message: message.text == 'Доход')
async def income_handler(message: types.Message):
    await IncomeState.income_input.set()

    await message.answer(text='ДОХОД:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text='Введите ваш доход', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Расход')
async def expenditure_handler(message: types.Message):
    await ExpenditureState.expenditure_input.set()

    await message.answer(text='РАСХОД:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text='Введите ваш расход', reply_markup=BUTTON_CANCEL)


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_input(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()

    await callback_query.message.answer(text='Отменено', reply_markup=BUTTON_MANAGE_MONEY)
    await callback_query.answer()


@dp.message_handler(lambda message: message.text == 'Категории')
async def categories_show_handler(message: types.Message):
    all_categories = await _show_all_categories(message.from_user.username)

    await message.answer(text='Вот список текущих категорий:\n' + all_categories, reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(lambda message: message.text == 'Добавить категорию')
async def categories_add_handler(message: types.Message):
    await AddCategoryState.add_categories_input.set()

    await message.answer(text='НОВАЯ КАТЕГОРИЯ:', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text='Введите название новой категории', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Удалить категорию')
async def categories_delete_handler(message: types.Message):

    await DeleteCategoryState.delete_categories_input.set()

    await message.answer(text='УДАЛЕНИЕ КАТЕГОРИИ:', reply_markup=types.ReplyKeyboardRemove())
    all_categories = await _show_all_categories(message.from_user.username)

    await message.answer(text='Мои категории:' + all_categories)
    await message.answer(text='Введите название категории', reply_markup=BUTTON_CANCEL)


@dp.message_handler(lambda message: message.text == 'Баланс')
async def balance_show_handler(message: types.Message):
    await message.answer(text='ВАШ ТЕКУЩИЙ БАЛАНС:')

    user_balance = await _get_balance(message.from_user.username)

    await message.answer(text=round(user_balance, 2), reply_markup=BUTTON_MANAGE_MONEY)


@dp.message_handler(state=IncomeState.income_input)
async def income_input_handler(message: types.Message, state: FSMContext):
    try:
        await validate_income_and_expenditure(user_input=message.text, username=message.from_user.username)
    except UnsupportedInput:
        await message.answer(text=USER_INPUT_RULE, reply_markup=BUTTON_MANAGE_MONEY)
    except ValueError:
        await message.answer(text=FLOAT_NUMBER_ERROR, reply_markup=BUTTON_MANAGE_MONEY)
    else:
        quantity, category = message.text.split()
        await _add_income(
            username=message.from_user.username,
            quantity=float(quantity),
            category=category.lower()
        )
        await message.answer(text='Новая запись:')
        await message.answer(text=f'ДОХОД {message.text}', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.reset_state()


@dp.message_handler(state=ExpenditureState.expenditure_input)
async def expenditure_input_handler(message: types.Message, state: FSMContext):
    try:
        await validate_income_and_expenditure(user_input=message.text, username=message.from_user.username)
    except UnsupportedInput:
        await message.answer(text=USER_INPUT_RULE, reply_markup=BUTTON_MANAGE_MONEY)
    except ValueError:
        await message.answer(text=FLOAT_NUMBER_ERROR, reply_markup=BUTTON_MANAGE_MONEY)
    else:
        quantity, category = message.text.split()
        await _add_expenditure(
            username=message.from_user.username,
            quantity=float(quantity),
            category=category.lower()
        )
        await message.answer(text='Новая запись:')
        await message.answer(text=f'РАСХОД {message.text}', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.reset_data()


@dp.message_handler(state=AddCategoryState.add_categories_input)
async def add_categories_input_handler(message: types.Message, state: FSMContext):
    try:
        await category_already_exist(category=message.text)
    except CategoryAlreadyExist:
        await message.answer(text='Посмотрите внимательно, кажется такая категория уже существует!', reply_markup=BUTTON_MANAGE_MONEY)
    else:
        await _add_new_category(category_name=message.text.lower(), username=message.from_user.username)
        await message.answer(text='Категория успешно добавлена!', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.reset_state()


@dp.message_handler(state=DeleteCategoryState.delete_categories_input)
async def delete_categories_input_handler(message: types.Message, state: FSMContext):
    try:
        await category_does_not_exist(category=message.text)
    except CategoryDoesNotExist:
        await message.answer(text='Мне кажется или такой категории нет?', reply_markup=BUTTON_MANAGE_MONEY)
    else:
        await _delete_category(username=message.from_user.username, category=message.text.lower())
        await message.answer(text='Категория успешно удалена!', reply_markup=BUTTON_MANAGE_MONEY)
    finally:
        await state.reset_state()
