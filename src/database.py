from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from typing import Generator

from .config import DB_URL


engine = create_async_engine(DB_URL, echo=True)
async_sessioin_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_sessioin_maker()
        yield session
    finally:
        await session.close()
