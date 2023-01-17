import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from db.db import Base, db_session


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created = Column(DateTime, default=func.now())

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()
