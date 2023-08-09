from sqlalchemy import insert, select, update, delete, and_

from user.models import User
from accounting.models import Categories, Accounting, OperationType
from .service import _execute_insert_update_delete_command, _execute_select_command
from main import redis


async def _add_new_category(category_name: str, username: str):
    statemant = insert(Categories).values(name=category_name, user_id=username)
    await _execute_insert_update_delete_command(statemant)

    categories = await redis.get(name=username + 'categories')
    await redis.set(name=username + 'categories', value=categories.decode("utf-8") + f'\n{category_name.capitalize()}')


async def _show_all_categories(username: str):
    response = await redis.get(name=username + 'categories')
    if not response:
        statemant = select(Categories).where(Categories.user_id == username)
        response = await _execute_select_command(statemant)
        response = ('\n').join(category.name.capitalize() for category in response)

        await redis.set(name=username + 'categories', value=response)
        return response

    return response.decode("utf-8")


async def _get_balance(username: str):
    response = await redis.get(name=username)
    if not response:
        statemant = select(User).where(User.username == username)
        response = await _execute_select_command(statemant)
        response = response[0].balance
        await redis.set(name=username, value=response)

    return float(response)


async def _add_income(username: str, category: str, quantity: float):
    statemant = insert(Accounting).values(
        user_id=username,
        quantity=quantity,
        categories=category,
        operation_type=OperationType.income
    )
    await _execute_insert_update_delete_command(statemant)

    statemant = update(User).where(User.username == username).values(balance=User.balance + quantity)
    await _execute_insert_update_delete_command(statemant)

    current_balance = await redis.get(name=username)
    await redis.set(name=username, value=float(current_balance) + quantity)


async def _add_expenditure(username: str, category: str, quantity: float):
    statemant = insert(Accounting).values(
        user_id=username,
        quantity=quantity,
        categories=category,
        operation_type=OperationType.expenditure
    )
    await _execute_insert_update_delete_command(statemant)

    statemant = update(User).where(User.username == username).values(balance=User.balance - quantity)
    await _execute_insert_update_delete_command(statemant)

    current_balance = await redis.get(name=username)
    await redis.set(name=username, value=float(current_balance) - quantity)


async def _delete_category(username: str, category: str):
    statemant = delete(Categories).where(and_(Categories.user_id == username, Categories.name == category))
    await _execute_insert_update_delete_command(statemant)

    categories = await redis.get(name=username + 'categories')
    await redis.set(name=username + 'categories', value=categories.decode("utf-8").replace(f'\n{category.capitalize()}', ''))


async def _get_category(category: str):
    statemant = select(Categories).where(Categories.name == category)

    return await _execute_select_command(statemant)
