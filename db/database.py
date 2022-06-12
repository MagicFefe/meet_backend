from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncConnection
from db.enitites.base_class import Base
from sqlalchemy.schema import MetaData
from typing import AsyncIterator
from sqlalchemy.orm import sessionmaker
from config import DB_URL


class Database:
    def __init__(self) -> None:
        self.engine: AsyncEngine = create_async_engine(DB_URL, echo=True)
        self.session_maker: sessionmaker = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_maker() as session:
            yield session

    async def init_tables(self) -> None:
        async with self.engine.begin() as connection:
            conn: AsyncConnection = connection
            meta: MetaData = Base.metadata
            await conn.run_sync(meta.create_all)
