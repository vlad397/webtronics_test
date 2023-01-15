from schemas.base import BaseSchema


class PostBodySchema(BaseSchema):
    """Сериализатор входных данных для создания поста"""

    header: str
    description: str
