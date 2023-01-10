from fastapi import APIRouter

from .login import router as login_router
from .refresh_token import router as refresh_router
from .registration import router as register_router

router = APIRouter(prefix="/v1")
router.include_router(login_router)
router.include_router(register_router)
router.include_router(refresh_router)
