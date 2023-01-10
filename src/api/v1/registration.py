from http import HTTPStatus
from typing import Any

from fastapi import APIRouter

from db.db_models import Users
from schemas.body import UserRegisterBodySchema
from schemas.response import Message, UserResponseSchema
from svc.handlers.user_handler import hash_password

router = APIRouter()


@router.post(
    "/register/",
    description="Registration method",
    status_code=HTTPStatus.CREATED,
    responses={201: {"model": UserResponseSchema}, 400: {"model": Message}},
)
def register(body: UserRegisterBodySchema) -> Any:
    if Users.find_by_email(body.email):
        return {"msg": "Such email already exists"}, HTTPStatus.BAD_REQUEST

    if Users.find_by_username(body.username):
        return {"msg": "Such username already exists"}, HTTPStatus.BAD_REQUEST

    body.password = hash_password(body.password)
    user = Users(**body.dict())
    user.save()

    return UserResponseSchema(id=str(user.id), username=str(user.username), email=str(user.email)), HTTPStatus.CREATED
