from aiogram import types

BUTTON_INCOME = types.KeyboardButton('Доход')
BUTTON_EXPENSE = types.KeyboardButton('Расход')
BUTTON_CANCEL = types.InlineKeyboardButton('Отмена', callback_data='cancel')
BUTTON_SHOW_CATEGORIES = types.KeyboardButton('Категории')
BUTTON_ADD_CATEGORIES = types.KeyboardButton('Добавить категорию')
BUTTON_DELETE_CATEGORIES = types.KeyboardButton('Удалить категорию')
BUTTON_BALANCE = types.KeyboardButton('Баланс')

BUTTON_MANAGE_MONEY = types.ReplyKeyboardMarkup(
    keyboard=[[BUTTON_BALANCE],
              [BUTTON_INCOME, BUTTON_EXPENSE],
              [BUTTON_SHOW_CATEGORIES, BUTTON_ADD_CATEGORIES, BUTTON_DELETE_CATEGORIES]],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

BUTTON_CANCEL = types.InlineKeyboardMarkup().add(BUTTON_CANCEL)
