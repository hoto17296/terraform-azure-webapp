from os import getenv

import asyncpg
from azure.identity import DefaultAzureCredential
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

DEBUG = bool(int(getenv("DEBUG", "0")))


async def get_connection() -> asyncpg.Connection:
    if getenv("DATABASE_URL"):
        return await asyncpg.connect(getenv("DATABASE_URL"))
    if getenv("DATABASE_HOST") and getenv("DATABASE_MS_ENTRA_AUTH_PRINCIPAL_NAME"):
        return await asyncpg.connect(
            host=getenv("DATABASE_HOST"),
            port=getenv("DATABASE_PORT", 5432),
            username=getenv("DATABASE_MS_ENTRA_AUTH_PRINCIPAL_NAME"),
            password=DefaultAzureCredential().get_token("https://ossrdbms-aad.database.windows.net/.default").token,
            database=getenv("DATABASE_DATABASE", "postgres"),
        )
    raise Exception("No valid database connection information")


engine = create_async_engine("postgresql+asyncpg://", async_creator=get_connection, echo=DEBUG)
AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionMaker() as session:
        yield session
