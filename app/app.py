import jwt
from fastapi import Depends, FastAPI, Request, Response
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


@app.get("/me")
async def me(request: Request):
    access_token = request.headers.get("x-ms-token-aad-access-token")
    id_token = request.headers.get("x-ms-token-aad-id-token")
    if access_token is None or id_token is None:
        return Response(status_code=401)
    return {
        "access_token": jwt.decode(access_token, options={"verify_signature": False}),
        "id_token": jwt.decode(id_token, options={"verify_signature": False}),
    }
