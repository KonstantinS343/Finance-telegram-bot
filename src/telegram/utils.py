from aiogram import types

from telegram import buttons
from main import bot, _
from .messages import TELEGRAM_USERNAME_EXISTANCE_MESSAGE
from middleware.user import _add_new_user
from middleware.general_handlers import (
    check_telegram_username,
    check_user_existence
)
from exception import (
    UserAlreadyExists,
    UserNameNotDefined
)


def auth(func):
    async def wrapper(message: types.Message):
        try:
            await check_telegram_username(username=message.from_user.username)
            await check_user_existence(username=message.from_user.username)
        except UserNameNotDefined:
            await message.answer(text=_(TELEGRAM_USERNAME_EXISTANCE_MESSAGE), reply_markup=await buttons.get_button_manage_money())
        except UserAlreadyExists:
            await func(message)
        else:
            await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAIxgmR_WduWkzBmN4xogt4TSPMCiukoAAI2FgACcmugS6XaTV2HP2QpLwQ')
            await _add_new_user(username=message.from_user.username)
            await func(message)

    return wrapper
