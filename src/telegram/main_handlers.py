from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram import buttons
from main import dp, _
from telegram.states import (
    IncomeState,
    ExpenditureState,
)
from .messages import FLOAT_NUMBER_ERROR
from middleware.accounting import (
    _get_balance,
    _add_income,
    _add_expenditure,
)
from middleware.accounting import _show_all_categories


@dp.message_handler(lambda message: message.text == _('➕ Доход'))
async def income_handler(message: types.Message):
    await IncomeState.income_input.set()

    await message.answer(text=_('ДОХОД:'), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=_('Введите ваш доход'))


@dp.message_handler(lambda message: message.text == _('➖ Расход'))
async def expenditure_handler(message: types.Message):
    await ExpenditureState.expenditure_input.set()

    await message.answer(text=_('РАСХОД:'), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=_('Введите ваш расход'))


@dp.message_handler(lambda message: message.text == _('📊 Баланс'))
async def balance_show_handler(message: types.Message):
    await message.answer(text=_('ВАШ ТЕКУЩИЙ БАЛАНС:'))

    user_balance = await _get_balance(message.from_user.username)

    await message.answer(text=round(user_balance, 2), reply_markup=await buttons.get_button_manage_money())


@dp.message_handler(state=IncomeState.income_input)
async def income_input_handler(message: types.Message, state: FSMContext):
    try:
        total = float(message.text)
    except ValueError:
        await message.answer(text=_(FLOAT_NUMBER_ERROR), reply_markup=await buttons.get_button_manage_money())
    else:
        await IncomeState.category_input.set()
        all_categories = await _show_all_categories(message.from_user.username)
        await message.answer(text=_('Введите категорию'), reply_markup=await buttons.categories_buttons(categories=all_categories))
        await state.update_data(total=total)
        await state.update_data(username=message.from_user.username)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('category'), state=IncomeState.category_input)
async def income_category_input_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    total = data.get('total')
    username = data.get('username')
    text = callback_query.data.replace('category_', '').lower()
    await _add_income(
        username=username,
        category=text,
        quantity=total
    )

    await callback_query.message.edit_text(text=_('Новая запись:'))
    await callback_query.message.answer(text=_('ДОХОД') + f' <b>{total} {text}</b>', reply_markup=await buttons.get_button_manage_money())

    await state.reset_state()
    await callback_query.answer()


@dp.message_handler(state=ExpenditureState.expenditure_input)
async def expenditure_input_handler(message: types.Message, state: FSMContext):
    try:
        total = float(message.text)
    except ValueError:
        await message.answer(text=_(FLOAT_NUMBER_ERROR), reply_markup=await buttons.get_button_manage_money())
    else:
        await ExpenditureState.category_input.set()
        all_categories = await _show_all_categories(message.from_user.username)
        await message.answer(text=_('Введите категорию'), reply_markup=await buttons.categories_buttons(categories=all_categories))
        await state.update_data(total=total)
        await state.update_data(username=message.from_user.username)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('category'), state=ExpenditureState.category_input)
async def expenditure_category_input_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    total = data.get('total')
    username = data.get('username')
    text = callback_query.data.replace('category_', '').lower()
    await _add_expenditure(
        username=username,
        category=text,
        quantity=total
    )

    await callback_query.message.edit_text(text=_('Новая запись:'))
    await callback_query.message.answer(text=_('РАСХОД') + f' <b>{total} {text}</b>', reply_markup=await buttons.get_button_manage_money())

    await state.reset_state()
    await callback_query.answer()
