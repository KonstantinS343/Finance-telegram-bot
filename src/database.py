from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URL


engine = create_async_engine(DB_URL, echo=True)
async_sessioin_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
