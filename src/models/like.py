import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models.base import BaseModel



class Like(BaseModel):
    __tablename__ = "like"
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), default=uuid.uuid4, nullable=False, primary_key=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), default=uuid.uuid4, nullable=False, primary_key=True)

    def __str__(self):
        return f"User - {self.user_id}, Post - {self.post_id}"