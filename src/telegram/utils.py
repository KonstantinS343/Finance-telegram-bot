from aiogram.dispatcher.filters.state import State, StatesGroup


class UserInput(StatesGroup):
    income_input = State()
    expenditure_input = State()
    add_categories_input = State()
    delete_categories_input = State()
