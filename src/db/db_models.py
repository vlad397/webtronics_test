import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from db.db import Base, db_session


class Users(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(length=256), nullable=False, unique=True)
    password = Column(String(length=256), nullable=False)
    email = Column(String(length=256), nullable=False, unique=True)

    def __init__(self, username, password, email) -> None:
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def find_by_user_id(cls, user_id: str):
        return cls.query.filter_by(id=user_id).one_or_none()

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def __repr__(self):
        return self.username
