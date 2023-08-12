from aiogram import types

from telegram import buttons
from main import dp, _
from middleware.user import _language_locale


@dp.message_handler(commands=['language'])
async def change_language(message: types.Message):
    await message.answer(text=_('Выберите язык'), reply_markup=buttons.BUTTON_LANGUAGE)


@dp.message_handler(lambda message: message.text == _('🔄 Перезагрузить'))
async def reboot(message: types.Message):

    await message.answer(text=_('Ваш язык был изменен'), reply_markup=await buttons.get_button_manage_money())


@dp.message_handler(lambda message: message.text == '🇺🇸 English')
async def language_en(message: types.Message):

    await _language_locale(username=message.from_user.username, lang='en')
    await message.answer(text=_('Изменения вступили в силу', locale='en'), reply_markup=await buttons.get_reboot_button(lang='en'))


@dp.message_handler(lambda message: message.text == '🇷🇺 Русский')
async def language_ru(message: types.Message):

    await _language_locale(username=message.from_user.username, lang='ru')
    await message.answer(text=_('Изменения вступили в силу', locale='ru'), reply_markup=await buttons.get_reboot_button(lang='ru'))


@dp.message_handler(lambda message: message.text == '🇧🇾 Беларускі')
async def language_be(message: types.Message):

    await _language_locale(username=message.from_user.username, lang='be')
    await message.answer(text=_('Изменения вступили в силу', locale='be'), reply_markup=await buttons.get_reboot_button(lang='be'))
