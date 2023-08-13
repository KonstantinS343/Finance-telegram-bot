from .user import _get_current_user
from .accounting import _get_category
from exception import (
    UserAlreadyExists,
    UserNameNotDefined,
    CategoryDoesNotExist,
    CategoryAlreadyExist
)


async def check_user_existence(username: str):
    response = await _get_current_user(username=username)

    if response:
        raise UserAlreadyExists


async def check_telegram_username(username: str):

    if not username:
        raise UserNameNotDefined


async def category_does_not_exist(category: str, username: str):
    response = await _get_category(category=category, username=username)

    if not response:
        raise CategoryDoesNotExist


async def category_already_exist(category: str, username: str):
    response = await _get_category(category=category, username=username)

    if response:
        raise CategoryAlreadyExist
