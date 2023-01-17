from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "user_table"

    username = Column(String(length=256), nullable=False, unique=True)
    password = Column(String(length=256), nullable=False)
    email = Column(String(length=256), nullable=False, unique=True)
    post = relationship("Post", back_populates="author")
    liked_posts = relationship("Post", secondary="like_table", back_populates="users_who_like")
    disliked_posts = relationship("Post", secondary="dislike_table", back_populates="users_who_dislike")

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

    def get_liked_posts(self) -> list[str]:
        return [post.id for post in self.liked_posts]

    def get_disliked_posts(self) -> list[str]:
        return [post.id for post in self.disliked_posts]

    def __repr__(self):
        return self.username
