import uuid

from schemas.base import BaseSchema


class UserResponseSchema(BaseSchema):
    """Схема ответа при регистрации"""

    id: uuid.UUID
    username: str
    email: str
