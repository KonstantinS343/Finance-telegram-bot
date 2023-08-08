from sqlalchemy import insert, select


from user.models import User
from .service import _execute_insert_update_delete_command, _execute_select_command


async def _add_new_user(username: str):
    statemant = insert(User).values(username=username)
    await _execute_insert_update_delete_command(statemant)


async def _get_current_user(username: str):
    statemant = select(User).where(User.username == username)

    return await _execute_select_command(statemant)
