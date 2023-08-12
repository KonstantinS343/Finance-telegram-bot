from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram import buttons
from main import dp, bot, _
from .messages import (
    START_MESSAGE,
    TELEGRAM_USERNAME_EXISTANCE_MESSAGE
)
from middleware.user import _add_new_user
from middleware.general_handlers import (
    check_telegram_username,
    check_user_existence
)
from exception import (
    UserAlreadyExists,
    UserNameNotDefined
)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    try:
        await check_telegram_username(username=message.from_user.username)
        await check_user_existence(username=message.from_user.username)
    except UserNameNotDefined:
        await message.answer(text=_(TELEGRAM_USERNAME_EXISTANCE_MESSAGE), reply_markup=await buttons.get_button_manage_money())
    except UserAlreadyExists:
        await message.answer(text=_(START_MESSAGE), reply_markup=await buttons.get_button_manage_money())
    else:
        await _add_new_user(username=message.from_user.username)
        await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAIxgmR_WduWkzBmN4xogt4TSPMCiukoAAI2FgACcmugS6XaTV2HP2QpLwQ')
        await message.answer(text=_(START_MESSAGE), reply_markup=await buttons.get_button_manage_money())


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_input(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()

    await callback_query.message.answer(text=_('Отменено'), reply_markup=await buttons.get_button_manage_money())
    await callback_query.answer()
