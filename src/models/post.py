from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Post(BaseModel):
    __tablename__ = "post"
    __table_args__ = (UniqueConstraint("header", "author_id", name="unique_author_header"),)

    header = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    author = relationship("User", back_populates="post")
    likes_count = Column(Integer, default=0)
    dislikes_count = Column(Integer, default=0)
    users_who_like = relationship("User", secondary="like", back_populates="liked_posts")
    users_who_dislike = relationship("User", secondary="dislike", back_populates="disliked_posts")

    @classmethod
    def find_by_post_id(cls, post_id: str):
        return cls.query.filter_by(id=post_id).one_or_none()

    def get_like_list(self) -> list[str]:
        return [user.id for user in self.users_who_like]

    def get_dislike_list(self) -> list[str]:
        return [user.id for user in self.users_who_dislike]

    def __repr__(self):
        return self.header
