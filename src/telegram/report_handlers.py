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
from report.diagram import create_diagram
from report.email_send import email_report


@dp.message_handler(commands=['report'])
async def run_report(message: types.Message, state: FSMContext):
    await ReportState.time_interval.set()
    await message.answer(text=_('Выберите промежуток времени'), reply_markup=await buttons.time_interval_buttons())
    await state.update_data(username=message.from_user.username)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('time'), state=ReportState.time_interval)
async def report(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    text = callback_query.data.replace('time_', '').lower()
    accounts = await _get_accounts(username=username, time=text)
    lang = await _get_user_lang(username=username)
    create_report.delay(username=username, accounts=accounts, lang=lang)
    create_diagram.delay(username=username, accounts=accounts, lang=lang)
    await ReportState.send_place.set()
    await callback_query.message.edit_text(text=_('Отчет сформирован!'))
    await callback_query.message.answer(text=_('Выберите место для отправки отчета'), reply_markup=await buttons.get_report_buttons())


@dp.message_handler(state=ReportState.send_place)
async def report_send_place(message: types.Message, state: FSMContext):
    user_input = message.text

    if user_input == _('📧 Почта'):
        response = await _get_users_email(username=message.from_user.username)
        if response:
            await EmailState.reuse_email.set()
            await message.answer(text=_('У вас есть сохранненая почта, использовать её?'), reply_markup=await buttons.get_email_remember_buttons())
        else:
            await ReportState.email.set()
            await message.answer(text=_('Введите вашу почту'), reply_markup=await buttons.get_button_cancel())
    elif user_input == _('📌 Чат'):
        document = open(f'{os.path.dirname(__file__)}/../report/reports/{message.from_user.username}_report.xlsx', 'rb')
        await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=await buttons.get_button_manage_money())
        await bot.send_photo(chat_id=message.chat.id,
                             photo=types.InputFile(f'{os.path.dirname(__file__)}/../report/diagrams/{message.from_user.username}_general_diagram.png'))
        await message.answer(text=_('РАСХОД'), reply_markup=await buttons.get_button_manage_money())
        await bot.send_photo(chat_id=message.chat.id,
                             photo=types.InputFile(f'{os.path.dirname(__file__)}/../report/diagrams/{message.from_user.username}_expenditure_diagram.png'))
        await message.answer(text=_('ДОХОД'), reply_markup=await buttons.get_button_manage_money())
        await bot.send_photo(chat_id=message.chat.id,
                             photo=types.InputFile(f'{os.path.dirname(__file__)}/../report/diagrams/{message.from_user.username}_income_diagram.png'))
        await state.reset_state()
    else:
        await message.answer(text=_('Отменено'), reply_markup=await buttons.get_button_manage_money())
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


@dp.message_handler(lambda message: message.text == _('🕒 Последние 10 операций'))
async def last_ten_operations(message: types.Message):
    accounts = await _get_accounts(username=message.from_user.username, time='last')
    msg = str()
    for i in accounts:
        msg += '\n<b>📌' + i.created_at.strftime("%d/%m/%Y, %H:%M:%S") + '  ' + str(i.quantity) + ' => ' + i.categories + '</b>\n'

    await message.answer(text=_('🕒 Последние 10 операций') + ':\n' + msg, reply_markup=await buttons.get_button_manage_money())
