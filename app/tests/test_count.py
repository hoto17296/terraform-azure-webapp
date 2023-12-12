from models import AccessLog
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def test_count(db: AsyncSession):
    count = (await db.exec(select(func.count(AccessLog.id)))).one()
    assert count == 0

    db.add(AccessLog())
    await db.commit()

    count = (await db.exec(select(func.count(AccessLog.id)))).one()
    assert count == 1
