import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models.base import BaseModel


class Dislike(BaseModel):
    __tablename__ = "dislike"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="unique_user_post_dislike"),)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), default=uuid.uuid4, nullable=False)

    def __str__(self):
        return f"User - {self.user_id}, Post - {self.post_id}"
