import uuid

from schemas.base import BaseSchema


class UserResponseSchema(BaseSchema):
    id: uuid.UUID
    username: str
    email: str
