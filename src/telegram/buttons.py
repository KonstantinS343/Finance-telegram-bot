from aiogram import types

BUTTON_INCOME = types.KeyboardButton('Доход')
BUTTON_EXPENSE = types.KeyboardButton('Расход')
BUTTON_CANCEL = types.InlineKeyboardButton('Отмена', callback_data='cancel')

BUTTON_MANAGE_MONEY = types.ReplyKeyboardMarkup(
    keyboard=[[BUTTON_INCOME, BUTTON_EXPENSE]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

BUTTON_CANCEL = types.InlineKeyboardMarkup().add(BUTTON_CANCEL)
