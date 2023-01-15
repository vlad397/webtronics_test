from fastapi import APIRouter, Depends

from svc.handlers.user_handler import has_access

from .dislike import router as dislike_router
from .like import router as like_router
from .login import router as login_router
from .post import router as post_router
from .refresh_token import router as refresh_router
from .registration import router as register_router

PROTECTED = [Depends(has_access)]

router = APIRouter(prefix="/v1")
router.include_router(login_router, tags=["user"])
router.include_router(register_router, tags=["user"])
router.include_router(refresh_router, tags=["user"], dependencies=PROTECTED)
router.include_router(post_router, tags=["post"], dependencies=PROTECTED)
router.include_router(like_router, tags=["like"], dependencies=PROTECTED)
router.include_router(dislike_router, tags=["like"], dependencies=PROTECTED)
