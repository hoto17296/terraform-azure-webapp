from fastapi import Depends, FastAPI
from models import AccessLog
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import get_db_session

app = FastAPI()


@app.get("/")
async def root(db: AsyncSession = Depends(get_db_session)):
    db.add(AccessLog())
    await db.commit()
    statement = select(func.count(AccessLog.id))
    count = (await db.exec(statement)).one()
    return {"count": count}
