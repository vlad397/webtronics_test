from pydantic import BaseModel


class Message(BaseModel):
    """Схема ответа в виде сообщения"""

    message: str
