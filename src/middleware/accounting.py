from sqlalchemy import insert, select, update, and_, extract, desc

from datetime import datetime, timedelta

from user.models import User
from accounting.models import Categories, Accounting, OperationType
from .service import _execute_insert_update_delete_command, _execute_select_command
from redis_manager import redis


async def _add_new_category(category_name: str, username: str):
    statemant = select(Categories).where(and_(Categories.name == category_name))

    response = await _execute_select_command(statemant)

    if not response:
        statemant = insert(Categories).values(name=category_name, user_id=username)
        await _execute_insert_update_delete_command(statemant)
    else:
        await _enable_category(category=category_name, username=username)

    categories = await redis.get(name=username + 'categories')
    if categories:
        await redis.set(name=username + 'categories', value=categories.decode("utf-8") + f'\n{category_name.capitalize()}')
    else:
        await redis.set(name=username + 'categories', value=f'\n{category_name.capitalize()}')


async def _enable_category(username: str, category: str):
    statemant = (update(Categories)
                 .where(and_(Categories.user_id == username, Categories.name == category, Categories.is_active == False))
                 .values(is_active=True))
    await _execute_insert_update_delete_command(statemant)


async def _show_all_categories(username: str):
    response = await redis.get(name=username + 'categories')

    if response is None:
        statemant = select(Categories).where(and_(Categories.user_id == username, Categories.is_active == True))
        response = await _execute_select_command(statemant)
        response = '\n' + ('\n').join(category.name.capitalize() for category in response)

        await redis.set(name=username + 'categories', value=response)
        return response

    return response.decode("utf-8")


async def _get_balance(username: str):
    response = await redis.get(name=username)
    if response is None:
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
    statemant = (update(Categories)
                 .where(and_(Categories.user_id == username, Categories.name == category, Categories.is_active == True))
                 .values(is_active=False))
    await _execute_insert_update_delete_command(statemant)

    categories = await redis.get(name=username + 'categories')
    await redis.set(name=username + 'categories', value=categories.decode("utf-8").replace(f'\n{category.capitalize()}', ''))


async def _get_category(category: str, username: str):
    response = await redis.get(name=username + 'categories')
    if response is None:
        return None

    if category.capitalize() not in response.decode("utf-8"):
        return None

    return category


async def _get_accounts(username: str, time: str):
    if time == 'last':
        statement = select(Accounting).order_by(desc(Accounting.created_at)).limit(10)
    else:
        threshold_date = datetime.utcnow() - timedelta(days=int(time))
        statement = select(Accounting).where(and_(Accounting.user_id == username, extract('epoch', Accounting.created_at) >= threshold_date.timestamp()))
    return await _execute_select_command(statemant=statement)
