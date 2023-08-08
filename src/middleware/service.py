from database import async_sessioin_maker


async def _execute_insert_update_delete_command(statemant):
    async with async_sessioin_maker() as session:
        async with session.begin():

            await session.execute(statemant)


async def _execute_select_command(statemant):
    async with async_sessioin_maker() as session:
        async with session.begin():

            result = await session.execute(statemant)

    return result.scalars().all()
