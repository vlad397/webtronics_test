from datetime import timedelta
from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends

from core.config import AuthJWT, config
from schemas.response import JWTAccessToken, Message

router = APIRouter()


@router.post(
    "/refresh/",
    description="Refresh token method",
    responses={200: {"model": JWTAccessToken}, 400: {"model": Message}, 401: {"model": Message}},
)
def refresh(Authorize: AuthJWT = Depends()) -> Any:
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            return {"msg": "Could not refresh access token"}, HTTPStatus.BAD_REQUEST

        access_token = Authorize.create_access_token(
            subject=str(user_id), expires_time=timedelta(minutes=config.JWT_ACCESS_EXPIRE)
        )

    except Exception as e:
        error = e.__class__.__name__
        if error == "MissingTokenError":
            return {"msg": "Please provide refresh token"}, HTTPStatus.BAD_REQUEST
        if error == "JWTDecodeError":
            return {"msg": "Refresh token has expired"}, HTTPStatus.UNAUTHORIZED
        return {"msg": error}, HTTPStatus.BAD_REQUEST

    return JWTAccessToken(access_token=access_token), HTTPStatus.OK