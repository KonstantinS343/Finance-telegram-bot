from aiogram import types
from main import _


async def get_button_manage_money():
    button_income = types.KeyboardButton(_('➕ Доход'))
    button_expense = types.KeyboardButton(_('➖ Расход'))

    button_show_categories = types.KeyboardButton(_('🗂 Категории'))
    button_add_category = types.KeyboardButton(_('📥 Добавить категорию'))
    button_delete_category = types.KeyboardButton(_('📤 Удалить категорию'))
    button_balance = types.KeyboardButton(_('📊 Баланс'))

    button_manager = types.ReplyKeyboardMarkup(
        keyboard=[[button_balance],
                  [button_income, button_expense],
                  [button_show_categories, button_add_category, button_delete_category]],
        resize_keyboard=True,
        input_field_placeholder=_('Выберите действие')
    )

    return button_manager


async def get_button_cancel():
    button_cancel = types.InlineKeyboardButton(_('⬅️ Отмена'), callback_data='cancel')

    button_cancel = types.InlineKeyboardMarkup().add(button_cancel)

    return button_cancel


async def get_reboot_button(lang: str):
    button_reboot = types.KeyboardButton(_('🔄 Перезагрузить', locale=lang))

    button_reboot = types.ReplyKeyboardMarkup(
        keyboard=[[button_reboot]],
        resize_keyboard=True,
        input_field_placeholder=_('Перезагрузить', locale=lang)
    )

    return button_reboot


async def get_report_buttons():
    chat_button = types.KeyboardButton(_('📌 Чат'))
    email_button = types.KeyboardButton(_('📧 Почта'))

    report_button = types.ReplyKeyboardMarkup(
        keyboard=[[chat_button, email_button]],
        resize_keyboard=True
    )

    return report_button


async def get_email_remember_buttons():
    yes_button = types.KeyboardButton(_('⭕️ Да'))
    no_button = types.KeyboardButton(_('❌ Нет'))

    email_remember_button = types.ReplyKeyboardMarkup(
        keyboard=[[yes_button, no_button]],
        resize_keyboard=True
    )

    return email_remember_button


RU_BUTTON = types.KeyboardButton('🇷🇺 Русский')
BE_BUTTON = types.KeyboardButton('🇧🇾 Беларускі')
EN_BUTTON = types.KeyboardButton('🇺🇸 English')

BUTTON_LANGUAGE = types.ReplyKeyboardMarkup(
    keyboard=[[RU_BUTTON, BE_BUTTON, EN_BUTTON]],
    resize_keyboard=True
)
