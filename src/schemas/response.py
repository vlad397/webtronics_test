from pydantic import BaseModel

from .base import BaseSchema


class UserResponseSchema(BaseSchema):
    id: str
    username: str
    email: str


class JWTAccessToken(BaseModel):
    access_token: str


class JWTToken(JWTAccessToken):
    refresh_token: str


class Message(BaseModel):
    message: str
