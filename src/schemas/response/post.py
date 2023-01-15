import uuid

from schemas.body.post import PostBodySchema

from .user import UserResponseSchema


class PostsResponseSchema(PostBodySchema):
    """Схема ответа при запросе всех постов"""

    id: uuid.UUID


class PostCreateResponseSchema(PostBodySchema):
    """Схема ответа при создании поста"""

    id: uuid.UUID
    author: UserResponseSchema


class PostResponseSchema(PostCreateResponseSchema):
    """Схема ответа при запросе конкретного поста"""

    likes_count: int
    dislikes_count: int
    users_who_like: list[uuid.UUID | str]
    users_who_dislike: list[uuid.UUID | str]
