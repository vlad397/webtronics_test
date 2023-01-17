from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, Depends
from fastapi_jwt_auth.exceptions import InvalidHeaderError, JWTDecodeError, MissingTokenError
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from core.config import AuthJWT
from models.post import Post
from models.user import User
from schemas.body.post import PostBodySchema
from schemas.response.common import Message
from schemas.response.post import PostCreateResponseSchema, PostResponseSchema, PostsResponseSchema

router = APIRouter()


@router.post(
    "/post/",
    description="Create post",
    status_code=HTTPStatus.CREATED,
    responses={201: {"model": PostResponseSchema}, 400: {"model": Message}, 401: {"model": Message}},
)
def create_post(body: PostBodySchema, Authorize: AuthJWT = Depends()) -> Any:
    """Функция создания поста"""
    try:
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST

        user = User.find_by_user_id(str(user_id))
        if not user:
            return {"msg": "No such user"}, HTTPStatus.BAD_REQUEST

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

    return (
        PostCreateResponseSchema(header=body.header, description=body.description, id=post.id, author=user),
        HTTPStatus.CREATED,
    )


@router.get(
    "/post/",
    description="Get all posts",
    responses={
        200: {"model": list[PostsResponseSchema]},
        400: {"model": Message},
        401: {"model": Message},
        404: {"model": Message},
    },
)
def get_all_posts(Authorize: AuthJWT = Depends()) -> Any:
    """Функция получения всех постов"""
    try:
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST

        posts = Post.query.all()
        if not posts:
            return {"msg": "No posts yet"}, HTTPStatus.NOT_FOUND

    except MissingTokenError:
        return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST
    except JWTDecodeError:
        return {"msg": "Access token has expired"}, HTTPStatus.UNAUTHORIZED
    except InvalidHeaderError:
        return {"msg": "Wrong access token form"}, HTTPStatus.BAD_REQUEST

    return [
        PostsResponseSchema(
            header=body.header,
            description=body.description,
            id=body.id,
        )
        for body in posts
    ], HTTPStatus.OK


@router.get(
    "/post/{id}/",
    description="Get concrete post",
    responses={
        200: {"model": PostResponseSchema},
        400: {"model": Message},
        401: {"model": Message},
        404: {"model": Message},
    },
)
def get_post(id: str, Authorize: AuthJWT = Depends()) -> Any:
    """Функция получения конкретного поста"""
    try:
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST

        post = Post.find_by_post_id(id)
        if not post:
            return {"msg": "Post does not exist"}, HTTPStatus.NOT_FOUND

    except MissingTokenError:
        return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST
    except JWTDecodeError:
        return {"msg": "Access token has expired"}, HTTPStatus.UNAUTHORIZED
    except InvalidHeaderError:
        return {"msg": "Wrong access token form"}, HTTPStatus.BAD_REQUEST

    return (
        PostResponseSchema(
            header=post.header,
            description=post.description,
            id=post.id,
            author=post.author,
            likes_count=post.likes_count,
            dislikes_count=post.dislikes_count,
            users_who_like=post.get_like_list(),
            users_who_dislike=post.get_dislike_list(),
        ),
        HTTPStatus.OK,
    )


@router.patch(
    "/post/{id}/",
    description="Patch concrete post",
    responses={
        200: {"model": PostResponseSchema},
        400: {"model": Message},
        401: {"model": Message},
        404: {"model": Message},
    },
)
def patch_post(id: str, body: PostBodySchema, Authorize: AuthJWT = Depends()) -> Any:
    """Функция частичного изменения поста"""
    try:
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST

        post = Post.find_by_post_id(id)
        if not post:
            return {"msg": "No such post"}, HTTPStatus.NOT_FOUND

        if user_id != str(post.author_id):
            return {"msg": "You have no permissions"}, HTTPStatus.BAD_REQUEST

        for key, value in body.dict().items():
            setattr(post, key, value)

    except MissingTokenError:
        return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST
    except JWTDecodeError:
        return {"msg": "Access token has expired"}, HTTPStatus.UNAUTHORIZED
    except InvalidHeaderError:
        return {"msg": "Wrong access token form"}, HTTPStatus.BAD_REQUEST

    return (
        PostResponseSchema(
            header=post.header,
            description=post.description,
            id=post.id,
            author=post.author,
            likes_count=post.likes_count,
            dislikes_count=post.dislikes_count,
            users_who_dislike=post.users_who_dislike,
            users_who_like=post.users_who_like,
        ),
        HTTPStatus.OK,
    )


@router.delete(
    "/post/{id}/",
    description="Delete concrete post",
    responses={200: {"model": Message}, 400: {"model": Message}, 401: {"model": Message}, 404: {"model": Message}},
)
def delete_post(id: str, Authorize: AuthJWT = Depends()) -> Any:
    """Функция удаления поста"""
    try:
        Authorize.jwt_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST

        post = Post.find_by_post_id(id)
        if not post:
            return {"msg": "No such post"}, HTTPStatus.NOT_FOUND

        if user_id != str(post.author_id):
            return {"msg": "You have no permissions"}, HTTPStatus.BAD_REQUEST

        post.delete()

    except MissingTokenError:
        return {"msg": "Please provide access token"}, HTTPStatus.BAD_REQUEST
    except JWTDecodeError:
        return {"msg": "Access token has expired"}, HTTPStatus.UNAUTHORIZED
    except InvalidHeaderError:
        return {"msg": "Wrong access token form"}, HTTPStatus.BAD_REQUEST

    return {"msg": "Deleted"}, HTTPStatus.OK
