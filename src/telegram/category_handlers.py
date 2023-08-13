from aiogram import types
from aiogram.dispatcher import FSMContext

from telegram import buttons
from main import dp, _
from telegram.states import (
    AddCategoryState,
    DeleteCategoryState
)
from middleware.accounting import (
    _add_new_category,
    _show_all_categories,
    _delete_category
)
from middleware.general_handlers import (
    category_does_not_exist,
    category_already_exist
)
from exception import (
    CategoryDoesNotExist,
    CategoryAlreadyExist,)


@dp.message_handler(lambda message: message.text == _('🗂 Категории'))
async def categories_show_handler(message: types.Message):
    all_categories = await _show_all_categories(message.from_user.username)
    all_categories = all_categories.split('\n')
    all_categories = [i for i in all_categories if i != '']
    msg = str()
    for i in all_categories:
        msg += '\n<b>📌 ' + i + '\n</b>'

    await message.answer(text=_('Вот список текущих категорий:\n') + msg, reply_markup=await buttons.get_button_manage_money())


@dp.message_handler(lambda message: message.text == _('📥 Добавить категорию'))
async def categories_add_handler(message: types.Message):
    await AddCategoryState.add_categories_input.set()

    await message.answer(text=_('НОВАЯ КАТЕГОРИЯ:'), reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=_('Введите название новой категории'), reply_markup=await buttons.get_button_cancel())


@dp.message_handler(lambda message: message.text == _('📤 Удалить категорию'))
async def categories_delete_handler(message: types.Message, state: FSMContext):

    await DeleteCategoryState.delete_categories_input.set()

    all_categories = await _show_all_categories(message.from_user.username)
    await message.answer(text=_('Введите категорию'), reply_markup=await buttons.categories_buttons(categories=all_categories))
    await state.update_data(username=message.from_user.username)


@dp.message_handler(state=AddCategoryState.add_categories_input)
async def add_categories_input_handler(message: types.Message, state: FSMContext):
    try:
        await category_already_exist(category=message.text.lower(), username=message.from_user.username)
    except CategoryAlreadyExist:
        await message.answer(text=_('Посмотрите внимательно, кажется такая категория уже существует!'), reply_markup=await buttons.get_button_manage_money())
    else:
        await _add_new_category(category_name=message.text.lower(), username=message.from_user.username)
        await message.answer(text=_('Категория успешно добавлена!'), reply_markup=await buttons.get_button_manage_money())
    finally:
        await state.reset_state()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('category'), state=DeleteCategoryState.delete_categories_input)
async def delete_categories_input_handler(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get('username')
    text = callback_query.data.replace('category_', '').lower()

    try:
        await category_does_not_exist(category=text, username=username)
    except CategoryDoesNotExist:
        await callback_query.message.answer(text=_('Мне кажется или такой категории нет?'), reply_markup=await buttons.get_button_manage_money())
    else:
        await _delete_category(username=username, category=text)
        await callback_query.message.edit_text(text=_('Категория успешно удалена!'))
    finally:
        await state.reset_state()
        await callback_query.answer()
