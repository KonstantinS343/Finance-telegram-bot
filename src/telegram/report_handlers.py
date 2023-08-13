from aiogram import types
from aiogram.dispatcher import FSMContext

import os

from telegram import buttons
from main import dp, bot, _
from telegram.states import (
    ReportState,
    EmailState
)
from middleware.user import _insert_user_email, _get_users_email, _get_user_lang
from middleware.accounting import _get_accounts
from exception import EmailAlreadyExist
from report.table import create_report
from report.email_send import email_report
from .utils import auth


@dp.message_handler(commands=['report'])
@auth
async def report(message: types.Message):
    accounts = await _get_accounts(username=message.from_user.username)
    lang = await _get_user_lang(username=message.from_user.username)
    create_report.delay(username=message.from_user.username, accounts=accounts, lang=lang)
    await ReportState.send_place.set()
    await message.answer(text=_('Выберите место для отправки отчета'), reply_markup=await buttons.get_report_buttons())


@dp.message_handler(state=ReportState.send_place)
async def report_send_place(message: types.Message, state: FSMContext):
    user_input = message.text

    if user_input == _('📧 Почта'):
        await message.answer(text=_('В отчете отоборажается информация за последние 90 дней'), reply_markup=types.ReplyKeyboardRemove())
        response = await _get_users_email(username=message.from_user.username)
        if response:
            await EmailState.reuse_email.set()
            await message.answer(text=_('У вас есть сохранненая почта, использовать её?'), reply_markup=await buttons.get_email_remember_buttons())
        else:
            await ReportState.email.set()
            await message.answer(text=_('Введите вашу почту'), reply_markup=await buttons.get_button_cancel())
    else:
        document = open(f'{os.path.dirname(__file__)}/../report/reports/{message.from_user.username}_report.xlsx', 'rb')
        await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=await buttons.get_button_manage_money())
        await state.reset_state()


@dp.message_handler(state=ReportState.email)
async def send_report(message: types.Message, state: FSMContext):
    user_email = message.text
    await ReportState.remember_email.set()
    email_report.delay(username=message.from_user.username, user_email=user_email)
    await message.answer(text=_('Сохранить почту?'), reply_markup=await buttons.get_email_remember_buttons())
    await state.update_data(email=user_email)


@dp.message_handler(state=ReportState.remember_email)
async def remember_email(message: types.Message, state: FSMContext):
    user_input = message.text
    data = await state.get_data()
    email = data.get('email')

    if user_input == _('⭕️ Да'):
        try:
            await _insert_user_email(username=message.from_user.username, email=email)
        except EmailAlreadyExist:
            await message.answer(text=_('Похоже такая почта уже существует! Выберите другую'), reply_markup=await buttons.get_button_manage_money())

    await message.answer(text=_('Проверьте свою почту'), reply_markup=await buttons.get_button_manage_money())

    await state.reset_state()


@dp.message_handler(state=EmailState.reuse_email)
async def reuse_email(message: types.Message, state: FSMContext):
    user_input = message.text

    if user_input == _('⭕️ Да'):
        await state.reset_state()
        email = await _get_users_email(username=message.from_user.username)
        email_report.delay(username=message.from_user.username, user_email=email.decode('utf-8'))
        await message.answer(text=_('Проверьте свою почту'), reply_markup=await buttons.get_button_manage_money())
    else:
        await ReportState.email.set()
        await message.answer(text=_('Введите вашу почту'), reply_markup=await buttons.get_button_cancel())
