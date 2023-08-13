from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram import buttons
from main import dp, _
from .messages import HELP_MESSAGE


@dp.message_handler(lambda message: message.text == _('⚙️ Настройки'))
async def settings(message: types.Message, state: FSMContext):
    await state.update_data(username=message.from_user.username)
    await message.answer(text=_('⚙️ Настройки'), reply_markup=await buttons.settings_button())


@dp.callback_query_handler(text='help')
async def cancel_input(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text=_(HELP_MESSAGE))
    await callback_query.answer()
    await state.reset_state()
