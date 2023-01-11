from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends

from core.config import AuthJWT
from models.user import User
from schemas.response.common import Message
from schemas.body.post import PostBodySchema
from schemas.response.post import PostResponseSchema
from models.post import Post
from psycopg2.errors import UniqueViolation
from fastapi_jwt_auth.exceptions import MissingTokenError, JWTDecodeError
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError, PendingRollbackError

router = APIRouter()


@router.post(
    "/post/",
    description="Create post", status_code=HTTPStatus.CREATED,
    responses={201: {"model": PostResponseSchema}, 400: {"model": Message}, 401: {"model": Message}},
)
def create_post(body: PostBodySchema, Authorize: AuthJWT = Depends()) -> Any:
    try:
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()

        if not user_id:
            return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST

        user = User.find_by_user_id(str(user_id))

        post = Post(header=body.header, description=body.description, author_id=user.id, author=user)
        post.save()

    except MissingTokenError:
        return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST
    except JWTDecodeError:
        return {"msg": "Access token has expired"}, HTTPStatus.UNAUTHORIZED
    except PendingRollbackError:
        return {"msg": "You already have post with that header"}, HTTPStatus.BAD_REQUEST
    except (IntegrityError) as err:
        if isinstance(err.orig, UniqueViolation):
            return {"msg": "You already have post with that header"}, HTTPStatus.BAD_REQUEST
        return {"msg": err.__class__.__name__}, HTTPStatus.BAD_REQUEST

    return PostResponseSchema(
        header=body.header, description=body.description,
        id=str(post.id), author=user
    ), HTTPStatus.CREATED
