from datetime import datetime

from sqlmodel import Field, SQLModel


class AccessLog(SQLModel, table=True):
    __tablename__ = "access_log"

    id: int | None = Field(default=None, primary_key=True)
    request_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
