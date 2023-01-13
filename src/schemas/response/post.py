import uuid

from schemas.body.post import PostBodySchema

from .user import UserResponseSchema


class PostsResponseSchema(PostBodySchema):
    id: uuid.UUID


class PostCreateResponseSchema(PostBodySchema):
    id: uuid.UUID
    author: UserResponseSchema


class PostResponseSchema(PostCreateResponseSchema):
    likes_count: int
    dislikes_count: int
    users_who_like: list[uuid.UUID]
    users_who_dislike: list[uuid.UUID]
