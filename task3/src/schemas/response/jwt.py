from pydantic import BaseModel


class JWTAccessToken(BaseModel):
    """Схема ответа при обновлении access токена"""

    access_token: str


class JWTToken(JWTAccessToken):
    """Схема ответа при входе в аккаунт"""

    refresh_token: str
