from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram import buttons
from main import dp, _
from .messages import START_MESSAGE
from .utils import auth


@dp.message_handler(commands=['start'])
@auth
async def start_bot(message: types.Message):
    await message.answer(text=_(START_MESSAGE), reply_markup=await buttons.get_button_manage_money())


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_input(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()

    await callback_query.message.answer(text=_('Отменено'), reply_markup=await buttons.get_button_manage_money())
    await callback_query.answer()
