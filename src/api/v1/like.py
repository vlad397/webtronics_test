from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from core.config import AuthJWT
from models.dislike import Dislike
from models.like import Like
from models.post import Post
from models.user import User
from schemas.response.common import Message

router = APIRouter()


@router.post(
    "/like/{id}/",
    description="Like post",
    responses={200: {"model": Message}, 400: {"model": Message}, 401: {"model": Message}},
)
def like_post(id: str, Authorize: AuthJWT = Depends()) -> Any:
    """Функция проставления лайка"""
    try:
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST

        user = User.find_by_user_id(str(user_id))
        if not user:
            return {"msg": "No such user"}, HTTPStatus.BAD_REQUEST

        post = Post.find_by_post_id(id)
        if not post:
            return {"msg": "Post does not exist"}, HTTPStatus.NOT_FOUND

        if user_id == str(post.author_id):
            return {"msg": "You cannot like your own post"}, HTTPStatus.BAD_REQUEST

        like = Like.check_like(user_id=user_id, post_id=id)
        if like:
            return {"msg": "You have already liked that post"}, HTTPStatus.BAD_REQUEST

        like = Like(user_id=user_id, post_id=id)
        like.save()

        post.likes_count += 1
        post.save()

        # Если до этого пост был дизлайкнут, то нужно удалить дизлайк
        dislike = Dislike.check_dislike(post_id=id, user_id=user_id)
        if dislike:
            dislike.delete()
            post.dislikes_count -= 1
            post.save()

    except MissingTokenError:
        return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST
    except JWTDecodeError:
        return {"msg": "Access token has expired"}, HTTPStatus.UNAUTHORIZED
    except PendingRollbackError:
        return {"msg": "You have already liked that post"}, HTTPStatus.BAD_REQUEST
    except (IntegrityError) as err:
        if isinstance(err.orig, UniqueViolation):
            return {"msg": "You have already liked that post"}, HTTPStatus.BAD_REQUEST
        return {"msg": err.__class__.__name__}, HTTPStatus.BAD_REQUEST

    return {"msg": "Liked!"}, HTTPStatus.OK
