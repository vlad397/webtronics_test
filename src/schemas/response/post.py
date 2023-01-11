from schemas.body.post import PostBodySchema
from .user import UserResponseSchema
import uuid


class PostResponseSchema(PostBodySchema):
    id: str | uuid.UUID
    author: UserResponseSchema
