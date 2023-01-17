from logging import config as logging_config
from typing import List, Union

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, BaseSettings, Field, PostgresDsn, validator

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str = "webtronics"
    DB_NAME: str = Field(env="DB_NAME", default="postgres")
    DB_USER: str = Field(env="POSTGRES_USER", default="postgres")
    DB_PASSWORD: str = Field(env="POSTGRES_PASSWORD", default="pass")
    DB_HOST: str = Field(env="DB_HOST", default="localhost")
    DB_PORT: int = Field(env="DB_PORT", default=5432)
    PSQL_DATABASE_URI: Union[str, None] = None

    SALT: str = Field(env="SALT", default="salt")
    SECRET_KEY: str = Field(env="SECRET_KEY", default="secret_key")
    JWT_ALGORITHM: str = Field(env="JWT_ALGORITHM", default="HS256")
    JWT_ACCESS_EXPIRE: int = Field(env="JWT_ACCESS_EXPIRE", default=5)
    JWT_REFRESH_EXPIRE: int = Field(env="JWT_REFRESH_EXPIRE", default=60)

    @validator("PSQL_DATABASE_URI", pre=True)
    def build_db_uri(cls, v: Union[str, None], values: dict) -> str:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f"/{values.get('DB_NAME')}",
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()

database_uri = config.PSQL_DATABASE_URI


class JWTSettings(BaseModel):
    authjwt_algorithm: str = config.JWT_ALGORITHM
    authjwt_decode_algorithms: List[str] = [config.JWT_ALGORITHM]
    authjwt_secret_key: str = config.SECRET_KEY


@AuthJWT.load_config
def get_config():
    return JWTSettings()
