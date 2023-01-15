import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models.base import BaseModel


class Like(BaseModel):
    __tablename__ = "like_table"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user_table.id"), default=uuid.uuid4, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post_table.id"), default=uuid.uuid4, nullable=False)

    @classmethod
    def check_like(cls, post_id: str, user_id: str):
        return cls.query.filter_by(post_id=post_id, user_id=user_id).one_or_none()

    def __str__(self):
        return f"User - {self.user_id}, Post - {self.post_id}"
