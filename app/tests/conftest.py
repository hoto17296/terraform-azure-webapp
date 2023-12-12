import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

dsn = "postgresql+asyncpg://postgres:deadbeef@database/test"
engine = create_async_engine(dsn)
AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def db(scope="function"):
    async with AsyncSessionMaker() as session:
        await session.exec(text("DROP SCHEMA public CASCADE"))
        await session.exec(text("CREATE SCHEMA public"))
        with open("/database/ddl.sql", "rt") as f:
            for statement in f.read().split(";"):
                statement = statement.strip()
                if statement:
                    await session.exec(text(statement))
        yield session
