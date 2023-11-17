from fastapi import FastAPI
from database import get_connection

app = FastAPI()


@app.get("/")
async def root():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO access_log DEFAULT VALUES")
            cur.execute("SELECT COUNT(1) FROM access_log")
            (count,) = cur.fetchone()
        conn.commit()
    return {"count": count}
