from sqlalchemy import insert, select, update


from database import async_sessioin_maker
from user.models import User
from accounting.models import Categories, Accounting, OperationType


async def _execute_insert_update_command(statemant):
    async with async_sessioin_maker() as session:
        async with session.begin():

            await session.execute(statemant)


async def _execute_select_command(statemant):
    async with async_sessioin_maker() as session:
        async with session.begin():

            result = await session.execute(statemant)

    return result.scalars().all()


async def _add_new_user(username: str):
    statemant = insert(User).values(username=username)
    await _execute_insert_update_command(statemant)


async def _add_new_category(category_name: str, username: str):
    statemant = insert(Categories).values(name=category_name, user_id=username)
    await _execute_insert_update_command(statemant)


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
    await _execute_insert_update_command(statemant)

    statemant = update(User).where(User.username == username).values(balance=User.balance + quantity)
    await _execute_insert_update_command(statemant)


async def _add_expenditure(username: str, category: str, quantity: float):
    statemant = insert(Accounting).values(
        user_id=username,
        quantity=quantity,
        categories=category,
        operation_type=OperationType.expenditure
    )
    await _execute_insert_update_command(statemant)

    statemant = update(User).where(User.username == username).values(balance=User.balance - quantity)
    await _execute_insert_update_command(statemant)
