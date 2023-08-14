from aiogram import types
from main import _


async def get_button_manage_money(lang=None):
    button_income = types.KeyboardButton(_('➕ Доход', locale=lang))
    button_expense = types.KeyboardButton(_('➖ Расход', locale=lang))

    button_show_categories = types.KeyboardButton(_('🗂 Категории', locale=lang))
    button_add_category = types.KeyboardButton(_('📥 Добавить категорию', locale=lang))
    button_delete_category = types.KeyboardButton(_('📤 Удалить категорию', locale=lang))
    button_balance = types.KeyboardButton(_('📊 Баланс', locale=lang))
    button_settings = types.KeyboardButton(_('⚙️ Настройки', locale=lang))
    last_button = types.KeyboardButton(_('🕒 Последние 10 операций'))

    button_manager = types.ReplyKeyboardMarkup(
        keyboard=[[button_balance],
                  [button_income, button_expense],
                  [button_show_categories, button_add_category, button_delete_category],
                  [button_settings, last_button]],
        resize_keyboard=True,
        input_field_placeholder=_('Выберите действие', locale=lang)
    )

    return button_manager


async def get_button_cancel():
    button_cancel = types.InlineKeyboardButton(_('⬅️ Отмена'), callback_data='cancel')

    button_cancel = types.InlineKeyboardMarkup().add(button_cancel)

    return button_cancel


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


async def categories_buttons(categories):
    categories = categories.split('\n')
    keyboard = types.InlineKeyboardMarkup()
    for category in categories:
        keyboard.add(types.InlineKeyboardButton(category, callback_data=f'category_{category}'))
    keyboard.add(types.InlineKeyboardButton(_('⬅️ Отмена'), callback_data='cancel'))

    return keyboard


async def settings_button():
    button_language = types.InlineKeyboardButton(_('🌐 Язык'), callback_data='language')
    help_button = types.InlineKeyboardButton(_('❓ Помощь'), callback_data='help')

    button_cancel = types.InlineKeyboardMarkup().add(button_language).add(help_button)

    return button_cancel


async def time_interval_buttons():
    day_button = types.InlineKeyboardButton(_('День'), callback_data='time_1')
    month_button = types.InlineKeyboardButton(_('Месяц'), callback_data='time_30')
    year_button = types.InlineKeyboardButton(_('Год'), callback_data='time_365')

    time_button = types.InlineKeyboardMarkup().add(day_button, month_button, year_button)

    return time_button


RU_BUTTON = types.InlineKeyboardButton('🇷🇺 Русский', callback_data='ru')
BE_BUTTON = types.InlineKeyboardButton('🇧🇾 Беларускі', callback_data='be')
EN_BUTTON = types.InlineKeyboardButton('🇺🇸 English', callback_data='en')

BUTTON_LANGUAGE = types.InlineKeyboardMarkup().add(RU_BUTTON).add(BE_BUTTON).add(EN_BUTTON)
