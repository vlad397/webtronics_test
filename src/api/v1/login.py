from datetime import timedelta
from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends

from core.config import AuthJWT, config
from models.user import User
from schemas.body.user import UserLoginBodySchema
from schemas.response.jwt import JWTToken
from schemas.response.common import Message
from svc.handlers.user_handler import validate_pass

router = APIRouter()


@router.post("/login/", description="Login method", responses={200: {"model": JWTToken}, 400: {"model": Message}})
def login(body: UserLoginBodySchema, Authorize: AuthJWT = Depends()) -> Any:
    user = User.find_by_username(body.username)

    if not user:
        return {"msg": "No such user"}, HTTPStatus.BAD_REQUEST

    if not validate_pass(user.password, body.password):
        return {"msg": "Wrong password"}, HTTPStatus.BAD_REQUEST

    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=config.JWT_ACCESS_EXPIRE)
    )
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(minutes=config.JWT_REFRESH_EXPIRE)
    )
    return JWTToken(access_token=access_token, refresh_token=refresh_token), HTTPStatus.OK
