from os import getenv

from azure.identity import DefaultAzureCredential
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

DEBUG = bool(int(getenv("DEBUG", "0")))

if getenv("DATABASE_URL"):
    dsn = getenv("DATABASE_URL")
elif getenv("DATABASE_HOST") and getenv("DATABASE_MS_ENTRA_AUTH_PRINCIPAL_NAME"):
    host = getenv("DATABASE_HOST")
    port = getenv("DATABASE_PORT", 5432)
    username = getenv("DATABASE_MS_ENTRA_AUTH_PRINCIPAL_NAME")
    password = DefaultAzureCredential().get_token("https://ossrdbms-aad.database.windows.net/.default").token
    database = getenv("DATABASE_DATABASE", "postgres")
    dsn = f"postgresql://{username}:{password}@{host}:{port}/{database}"
else:
    raise Exception("No valid database connection information")

engine = create_async_engine(dsn.replace("postgresql://", "postgresql+asyncpg://"), echo=DEBUG)
AsyncSessionMaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionMaker() as session:
        yield session
