from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import create_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.extra["pg"] = await create_pool()
    yield
    await app.extra["pg"].close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    async with app.extra["pg"].acquire() as conn:
        await conn.execute("INSERT INTO access_log DEFAULT VALUES")
        count = await conn.fetchval("SELECT COUNT(1) FROM access_log")
    return {"count": count}
