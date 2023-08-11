from aiogram import types
from aiogram.dispatcher import FSMContext

import os

from telegram.buttons import (
    get_button_manage_money,
    get_button_cancel,
    get_reboot_button,
    get_report_buttons,
    get_email_remember_buttons,
    BUTTON_LANGUAGE
)
from main import dp, bot, _
from telegram.states import (
    IncomeState,
    ExpenditureState,
    AddCategoryState,
    DeleteCategoryState,
    ReportState,
    EmailState
)
from .messages import (
    START_MESSAGE,
    TELEGRAM_USERNAME_EXISTANCE_MESSAGE,
    FLOAT_NUMBER_ERROR
)
from middleware.user import _add_new_user, _language_locale, _insert_user_email, _get_users_email
from middleware.accounting import (
    _add_new_category,
    _show_all_categories,
    _get_balance,
    _add_income,
    _add_expenditure,
    _delete_category,
    _get_accounts
)
from middleware.general_handlers import (
    check_telegram_username,
    check_user_existence,
    category_does_not_exist,
    category_already_exist,
    check_or_add_category
)
from exception import (
    UserAlreadyExists,
    UserNameNotDefined,
    CategoryDoesNotExist,
    CategoryAlreadyExist,
    EmailAlreadyExist
)
from report.table import create_report
from report.email_send import email_report


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    try:
        await check_telegram_username(username=message.from_user.username)
        await check_user_existence(username=message.from_user.username)
    except UserNameNotDefined:
        await message.answer(text=_(TELEGRAM_USERNAME_EXISTANCE_MESSAGE), reply_markup=await get_button_manage_money())
    except UserAlreadyExists:
        await message.answer(text=_(START_MESSAGE), reply_markup=await get_button_manage_money())
    else:
        await _add_new_user(username=message.from_user.username)
        await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAIxgmR_WduWkzBmN4xogt4TSPMCiukoAAI2FgACcmugS6XaTV2HP2QpLwQ')
        await message.answer(text=_(START_MESSAGE), reply_markup=await get_button_manage_money())


@dp.message_handler(commands=['report'])
async def report(message: types.Message):
    try:
        await check_telegram_username(username=message.from_user.username)
        await check_user_existence(username=message.from_user.username)
    except UserNameNotDefined:
        await message.answer(text=_(TELEGRAM_USERNAME_EXISTANCE_MESSAGE), reply_markup=await get_button_manage_money())
    except UserAlreadyExists:
        pass
    else:
        await _add_new_user(username=message.from_user.username)
    finally:
        accounts = await _get_accounts(username=message.from_user.username)
        create_report.delay(username=message.from_user.username, accounts=accounts)
        await ReportState.send_place.set()
        await message.answer(text=_('Выберите место для отправки отчета'), reply_markup=await get_report_buttons())


@dp.message_handler(commands=['language'])
async def change_language(message: types.Message):
    await message.answer(text=_('Выберите язык'), reply_markup=BUTTON_LANGUAGE)


@dp.message_handler(lambda message: message.text == _('Перезагрузить'))
async def reboot(message: types.Message):

    await message.answer(text=_('Ваш язык был изменен'), reply_markup=await get_button_manage_money())


@dp.message_handler(lambda message: message.text == 'English')
async def language_en(message: types.Message):

    await _language_locale(username=message.from_user.username, lang='en')
    await message.answer(text=_('Изменения вступили в силу', locale='en'), reply_markup=await get_reboot_button(lang='en'))


@dp.message_handler(lambda message: message.text == 'Русский')
async def language_ru(message: types.Message):

    await _language_locale(username=message.from_user.username, lang='ru')
    await message.answer(text=_('Изменения вступили в силу', locale='ru'), reply_markup=await get_reboot_button(lang='ru'))


@dp.message_handler(lambda message: message.text == 'Беларускі')
async def language_be(message: types.Message):

    await _language_locale(username=message.from_user.username, lang='be')
    await message.answer(text=_('Изменения вступили в силу', locale='be'), reply_markup=await get_reboot_button(lang='be'))


@dp.message_handler(lambda message: message.text == _('Доход'))
async def income_handler(message: types.Message):
    await IncomeState.income_input.set()

    await message.answer(text=_('ДОХОД:'), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=_('Введите ваш доход'), reply_markup=await get_button_cancel())


@dp.message_handler(lambda message: message.text == _('Расход'))
async def expenditure_handler(message: types.Message):
    await ExpenditureState.expenditure_input.set()

    await message.answer(text=_('РАСХОД:'), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=_('Введите ваш расход'), reply_markup=await get_button_cancel())


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_input(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state()

    await callback_query.message.answer(text=_('Отменено'), reply_markup=await get_button_manage_money())
    await callback_query.answer()


@dp.message_handler(lambda message: message.text == _('Категории'))
async def categories_show_handler(message: types.Message):
    all_categories = await _show_all_categories(message.from_user.username)

    await message.answer(text=_('Вот список текущих категорий:\n') + all_categories, reply_markup=await get_button_manage_money())


@dp.message_handler(lambda message: message.text == _('Добавить категорию'))
async def categories_add_handler(message: types.Message):
    await AddCategoryState.add_categories_input.set()

    await message.answer(text=_('НОВАЯ КАТЕГОРИЯ:'), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=_('Введите название новой категории'), reply_markup=await get_button_cancel())


@dp.message_handler(lambda message: message.text == _('Удалить категорию'))
async def categories_delete_handler(message: types.Message):

    await DeleteCategoryState.delete_categories_input.set()

    await message.answer(text=_('УДАЛЕНИЕ КАТЕГОРИИ:'), reply_markup=types.ReplyKeyboardRemove())
    all_categories = await _show_all_categories(message.from_user.username)

    await message.answer(text=_('Мои категории:\n') + all_categories)
    await message.answer(text=_('Введите название категории'), reply_markup=await get_button_cancel())


@dp.message_handler(lambda message: message.text == _('Баланс'))
async def balance_show_handler(message: types.Message):
    await message.answer(text=_('ВАШ ТЕКУЩИЙ БАЛАНС:'))

    user_balance = await _get_balance(message.from_user.username)

    await message.answer(text=round(user_balance, 2), reply_markup=await get_button_manage_money())


@dp.message_handler(state=IncomeState.income_input)
async def income_input_handler(message: types.Message, state: FSMContext):
    try:
        total = float(message.text)
    except ValueError:
        await message.answer(text=_(FLOAT_NUMBER_ERROR), reply_markup=await get_button_manage_money())
    else:
        await IncomeState.category_input.set()
        await message.answer(text=_('Введите название категории'), reply_markup=await get_button_cancel())
        await state.update_data(total=total)


@dp.message_handler(state=IncomeState.category_input)
async def income_category_input_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    total = data.get('total')
    await check_or_add_category(category=message.text.lower(), username=message.from_user.username)
    await _add_income(
        username=message.from_user.username,
        category=message.text,
        quantity=total
    )

    await message.answer(text=_('Новая запись:'))
    await message.answer(text=_('ДОХОД') + f' {total} {message.text}', reply_markup=await get_button_manage_money())

    await state.reset_state()


@dp.message_handler(state=ExpenditureState.expenditure_input)
async def expenditure_input_handler(message: types.Message, state: FSMContext):
    try:
        total = float(message.text)
    except ValueError:
        await message.answer(text=_(FLOAT_NUMBER_ERROR), reply_markup=await get_button_manage_money())
    else:
        await ExpenditureState.category_input.set()
        await message.answer(text=_('Введите название категории'), reply_markup=await get_button_cancel())
        await state.update_data(total=total)


@dp.message_handler(state=ExpenditureState.category_input)
async def expenditure_category_input_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    total = data.get('total')
    await check_or_add_category(category=message.text.lower(), username=message.from_user.username)
    await _add_expenditure(
        username=message.from_user.username,
        category=message.text,
        quantity=total
    )

    await message.answer(text=_('Новая запись:'))
    await message.answer(text=_('РАСХОД') + f' {total} {message.text}', reply_markup=await get_button_manage_money())

    await state.reset_state()


@dp.message_handler(state=AddCategoryState.add_categories_input)
async def add_categories_input_handler(message: types.Message, state: FSMContext):
    try:
        await category_already_exist(category=message.text.lower(), username=message.from_user.username)
    except CategoryAlreadyExist:
        await message.answer(text=_('Посмотрите внимательно, кажется такая категория уже существует!'), reply_markup=await get_button_manage_money())
    else:
        await _add_new_category(category_name=message.text.lower(), username=message.from_user.username)
        await message.answer(text=_('Категория успешно добавлена!'), reply_markup=await get_button_manage_money())
    finally:
        await state.reset_state()


@dp.message_handler(state=DeleteCategoryState.delete_categories_input)
async def delete_categories_input_handler(message: types.Message, state: FSMContext):
    try:
        await category_does_not_exist(category=message.text.lower(), username=message.from_user.username)
    except CategoryDoesNotExist:
        await message.answer(text=_('Мне кажется или такой категории нет?'), reply_markup=await get_button_manage_money())
    else:
        await _delete_category(username=message.from_user.username, category=message.text.lower())
        await message.answer(text=_('Категория успешно удалена!'), reply_markup=await get_button_manage_money())
    finally:
        await state.reset_state()


@dp.message_handler(state=ReportState.send_place)
async def report_send_place(message: types.Message, state: FSMContext):
    user_input = message.text

    if user_input == _('Почта'):
        await message.answer(text=_('В отчете отоборажается информация за последние 90 дней'), reply_markup=types.ReplyKeyboardRemove())
        response = await _get_users_email(username=message.from_user.username)
        if response:
            await EmailState.reuse_email.set()
            await message.answer(text=_('У вас есть сохранненая почта, использовать её?'), reply_markup=await get_email_remember_buttons())
        else:
            await ReportState.email.set()
            await message.answer(text=_('Введите вашу почту'), reply_markup=await get_button_cancel())
    else:
        document = open(f'{os.path.dirname(__file__)}/../report/reports/{message.from_user.username}_report.xlsx', 'rb')
        await bot.send_document(chat_id=message.chat.id, document=document, reply_markup=await get_button_manage_money())
        await state.reset_state()


@dp.message_handler(state=ReportState.email)
async def send_report(message: types.Message, state: FSMContext):
    user_email = message.text
    await ReportState.remember_email.set()
    email_report.delay(username=message.from_user.username, user_email=user_email)
    await message.answer(text=_('Сохранить почту?'), reply_markup=await get_email_remember_buttons())
    await state.update_data(email=user_email)


@dp.message_handler(state=ReportState.remember_email)
async def remember_email(message: types.Message, state: FSMContext):
    user_input = message.text
    data = await state.get_data()
    email = data.get('email')

    if user_input == _('Да'):
        try:
            await _insert_user_email(username=message.from_user.username, email=email)
        except EmailAlreadyExist:
            await message.answer(text=_('Похоже такая почта уже существует! Выберите другую'), reply_markup=await get_button_manage_money())

    await message.answer(text=_('Проверьте свою почту'), reply_markup=await get_button_manage_money())

    await state.reset_state()


@dp.message_handler(state=EmailState.reuse_email)
async def reuse_email(message: types.Message, state: FSMContext):
    user_input = message.text

    if user_input == _('Да'):
        await state.reset_state()
        email = await _get_users_email(username=message.from_user.username)
        email_report.delay(username=message.from_user.username, user_email=email.decode('utf-8'))
        await message.answer(text=_('Проверьте свою почту'), reply_markup=await get_button_manage_money())
    else:
        await ReportState.email.set()
        await message.answer(text=_('Введите вашу почту'), reply_markup=await get_button_cancel())
