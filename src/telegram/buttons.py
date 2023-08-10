from aiogram import types
from main import _


async def get_button_manage_money():
    BUTTON_INCOME = types.KeyboardButton(_('Доход'))
    BUTTON_EXPENSE = types.KeyboardButton(_('Расход'))

    BUTTON_SHOW_CATEGORIES = types.KeyboardButton(_('Категории'))
    BUTTON_ADD_CATEGORIES = types.KeyboardButton(_('Добавить категорию'))
    BUTTON_DELETE_CATEGORIES = types.KeyboardButton(_('Удалить категорию'))
    BUTTON_BALANCE = types.KeyboardButton(_('Баланс'))

    BUTTON_MANAGE_MONEY = types.ReplyKeyboardMarkup(
        keyboard=[[BUTTON_BALANCE],
                  [BUTTON_INCOME, BUTTON_EXPENSE],
                  [BUTTON_SHOW_CATEGORIES, BUTTON_ADD_CATEGORIES, BUTTON_DELETE_CATEGORIES]],
        resize_keyboard=True,
        input_field_placeholder=_('Выберите действие')
    )

    return BUTTON_MANAGE_MONEY


async def get_button_cancel():
    BUTTON_CANCEL = types.InlineKeyboardButton(_('Отмена'), callback_data='cancel')

    BUTTON_CANCEL = types.InlineKeyboardMarkup().add(BUTTON_CANCEL)

    return BUTTON_CANCEL

RU_BUTTON = types.KeyboardButton('Русский')
BE_BUTTON = types.KeyboardButton('Беларускі')
EN_BUTTON = types.KeyboardButton('English')

BUTTON_LANGUAGE = types.ReplyKeyboardMarkup(
    keyboard=[[RU_BUTTON, BE_BUTTON, EN_BUTTON]],
    resize_keyboard=True
)
