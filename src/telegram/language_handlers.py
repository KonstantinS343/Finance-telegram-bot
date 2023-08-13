from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram import buttons
from main import dp, _
from middleware.user import _language_locale
from .states import LanguageState


@dp.callback_query_handler(text='language')
async def change_language(callback_query: types.CallbackQuery):
    await LanguageState.language.set()
    await callback_query.message.edit_text(text=_('Выберите язык'), reply_markup=buttons.BUTTON_LANGUAGE)


@dp.callback_query_handler(text='en', state=LanguageState.language)
async def language_en(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')

    await _language_locale(username=username, lang='en')
    await callback_query.message.edit_text(text=_('Ваш язык был изменен', locale='en'))
    await callback_query.message.answer(text=_('Изменения вступили в силу', locale='en'), reply_markup=await buttons.get_button_manage_money(lang='en'))
    await state.reset_state()


@dp.callback_query_handler(text='ru', state=LanguageState.language)
async def language_ru(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')

    await _language_locale(username=username, lang='ru')
    await callback_query.message.edit_text(text=_('Ваш язык был изменен', locale='ru'))
    await callback_query.message.answer(text=_('Изменения вступили в силу', locale='ru'), reply_markup=await buttons.get_button_manage_money(lang='ru'))
    await state.reset_state()


@dp.callback_query_handler(text='be', state=LanguageState.language)
async def language_be(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')

    await _language_locale(username=username, lang='be')
    await callback_query.message.edit_text(text=_('Ваш язык был изменен', locale='be'))
    await callback_query.message.answer(text=_('Изменения вступили в силу', locale='be'), reply_markup=await buttons.get_button_manage_money(lang='be'))
    await state.reset_state()
