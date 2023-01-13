import hashlib

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import AuthJWT, config

security = HTTPBearer()


def hash_password(password: str) -> str:
    hash_password = hashlib.md5(f"{password}{config.SALT}".encode()).hexdigest()
    return hash_password


def validate_pass(db_password, password: str) -> bool:
    hash_password = hashlib.md5(f"{password}{config.SALT}".encode()).hexdigest()
    return db_password == hash_password


def has_access(credentials: HTTPAuthorizationCredentials = Depends(security), Authorize: AuthJWT = Depends()):
    """Функция для отображения у защищенных ссылок в документации знака замка"""
    pass
