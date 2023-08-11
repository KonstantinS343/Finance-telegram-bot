from aiogram.dispatcher.filters.state import State, StatesGroup


class IncomeState(StatesGroup):
    income_input = State()
    category_input = State()


class ExpenditureState(StatesGroup):
    expenditure_input = State()
    category_input = State()


class AddCategoryState(StatesGroup):
    add_categories_input = State()


class DeleteCategoryState(StatesGroup):
    delete_categories_input = State()


class ReportState(StatesGroup):
    send_place = State()
    email = State()
