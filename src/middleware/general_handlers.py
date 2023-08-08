from .user import _get_current_user
from .accounting import _get_category, _add_new_category
from exception import (
    UserAlreadyExists,
    UserNameNotDefined,
    UnsupportedInput,
    CategoryDoesNotExist
)


async def check_user_existence(username: str):
    response = await _get_current_user(username=username)

    if response:
        raise UserAlreadyExists


async def check_telegram_username(username: str):

    if not username:
        raise UserNameNotDefined


async def check_or_add_category(category: str, username: str):
    response = await _get_category(category=category)

    if not response:
        await _add_new_category(category_name=category, username=username)


async def check_category_existance(category: str):
    response = await _get_category(category=category)

    if not response:
        raise CategoryDoesNotExist


async def validate_income_and_expenditure(user_input: str, username: str):
    try:
        quantity, category = user_input.split()
    except ValueError:
        raise UnsupportedInput

    if not isinstance(quantity, str) and not isinstance(category, str):
        raise UnsupportedInput

    quantity = float(quantity)

    await check_or_add_category(category, username)
