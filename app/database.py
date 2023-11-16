from os import getenv

import asyncpg
from azure.identity import DefaultAzureCredential


async def create_pool():
    if getenv("DATABASE_URL"):
        dsn = getenv("DATABASE_URL")
    elif getenv("DATABASE_HOST") and getenv("DATABASE_MS_ENTRA_AUTH_PRINCIPAL_NAME"):
        host = getenv("DATABASE_HOST")
        port = getenv("DATABASE_PORT", 5432)
        username = getenv("DATABASE_MS_ENTRA_AUTH_PRINCIPAL_NAME")
        password = DefaultAzureCredential().get_token("https://ossrdbms-aad.database.windows.net/.default")
        database = getenv("DATABASE_DATABASE", "postgres")
        dsn = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    return await asyncpg.create_pool(dsn)
