from aiogram import types
from main import _


async def get_button_manage_money():
    button_income = types.KeyboardButton(_('Доход'))
    button_expense = types.KeyboardButton(_('Расход'))

    button_show_categories = types.KeyboardButton(_('Категории'))
    button_add_category = types.KeyboardButton(_('Добавить категорию'))
    button_delete_category = types.KeyboardButton(_('Удалить категорию'))
    button_balance = types.KeyboardButton(_('Баланс'))

    button_manager = types.ReplyKeyboardMarkup(
        keyboard=[[button_balance],
                  [button_income, button_expense],
                  [button_show_categories, button_add_category, button_delete_category]],
        resize_keyboard=True,
        input_field_placeholder=_('Выберите действие')
    )

    return button_manager


async def get_button_cancel():
    button_cancel = types.InlineKeyboardButton(_('Отмена'), callback_data='cancel')

    button_cancel = types.InlineKeyboardMarkup().add(button_cancel)

    return button_cancel


async def get_reboot_button(lang: str):
    button_reboot = types.KeyboardButton(_('Перезагрузить', locale=lang))

    button_reboot = types.ReplyKeyboardMarkup(
        keyboard=[[button_reboot]],
        resize_keyboard=True,
        input_field_placeholder=_('Перезагрузить', locale=lang)
    )

    return button_reboot


RU_BUTTON = types.KeyboardButton('Русский')
BE_BUTTON = types.KeyboardButton('Беларускі')
EN_BUTTON = types.KeyboardButton('English')

BUTTON_LANGUAGE = types.ReplyKeyboardMarkup(
    keyboard=[[RU_BUTTON, BE_BUTTON, EN_BUTTON]],
    resize_keyboard=True
)
