from aiogram.dispatcher.filters.state import State, StatesGroup


class UserInput(StatesGroup):
    input = State()
