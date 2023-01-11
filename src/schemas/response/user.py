from schemas.base import BaseSchema
import uuid


class UserResponseSchema(BaseSchema):
    id: str | uuid.UUID
    username: str
    email: str
