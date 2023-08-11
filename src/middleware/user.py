from sqlalchemy import insert, select, update


from user.models import User
from .service import _execute_insert_update_delete_command, _execute_select_command
from redis_manager import redis
from exception import EmailAlreadyExist


async def _add_new_user(username: str):
    statemant = insert(User).values(username=username)
    await _execute_insert_update_delete_command(statemant)


async def _get_current_user(username: str):
    statemant = select(User).where(User.username == username)

    return await _execute_select_command(statemant)


async def _language_locale(username: str, lang: str):
    statemant = update(User).where(User.username == username).values(locale=lang)
    await _execute_insert_update_delete_command(statemant)

    await redis.set(name=username + ':lang', value=lang)


async def _get_user_lang(username: str):
    response = await redis.get(name=username + ':lang')

    try:
        response = response.decode("utf-8")
    except AttributeError:
        pass
    finally:
        return response


async def _get_users_email(username: str):
    response = await redis.get(name=username + ':email')

    return response


async def _insert_user_email(username: str, email: str):
    response = await redis.get(name=username + ':email')

    if response:
        raise EmailAlreadyExist

    statemant = update(User).where(User.username == username).values(email=email)
    await _execute_insert_update_delete_command(statemant)

    await redis.set(name=username + ':email', value=email)
