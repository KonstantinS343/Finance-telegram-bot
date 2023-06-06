from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BUTTON_INCOME = InlineKeyboardButton('Доход', callback_data='income')
BUTTON_EXPENSE = InlineKeyboardButton('Расход', callback_data='expenditure')
BUTTON_CANCEL = InlineKeyboardButton('Отмена', callback_data='cancel')

BUTTON_MANAGE_MONEY = InlineKeyboardMarkup().add(BUTTON_INCOME).add(BUTTON_EXPENSE)
BUTTON_CANCEL = InlineKeyboardMarkup().add(BUTTON_CANCEL)
