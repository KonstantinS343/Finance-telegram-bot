from sqlalchemy import insert, select, update, delete, and_

from user.models import User
from accounting.models import Categories, Accounting, OperationType
from .service import _execute_insert_update_delete_command, _execute_select_command


async def _add_new_category(category_name: str, username: str):
    statemant = insert(Categories).values(name=category_name, user_id=username)
    await _execute_insert_update_delete_command(statemant)


async def _show_all_categories(username: str):
    statemant = select(Categories).where(Categories.user_id == username)
    response = await _execute_select_command(statemant)

    return response


async def _get_balance(username: str):
    statemant = select(User).where(User.username == username)
    response = await _execute_select_command(statemant)

    return response


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


async def _delete_category(username: str, category: str):
    statemant = delete(Categories).where(and_(Categories.user_id == username, Categories.name == category))
    await _execute_insert_update_delete_command(statemant)


async def _get_category(category: str):
    statemant = select(Categories).where(Categories.name == category)

    return await _execute_select_command(statemant)
