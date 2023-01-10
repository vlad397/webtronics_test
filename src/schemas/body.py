import re

from pydantic import validator

from .base import BaseSchema


class UserLoginBodySchema(BaseSchema):
    username: str
    password: str


class UserRegisterBodySchema(UserLoginBodySchema):
    email: str

    @validator("email")
    def check_email_correct(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, v):
            return v
        raise ValueError("Wrong email format")

    @validator("username")
    def check_username_correct(cls, v):
        regex = "^[a-zA-Z0-9_.-]*$"
        if re.fullmatch(regex, v):
            return v
        raise ValueError("Wrong username format")
