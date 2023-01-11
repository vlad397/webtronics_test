from pydantic import BaseModel


class JWTAccessToken(BaseModel):
    access_token: str


class JWTToken(JWTAccessToken):
    refresh_token: str
