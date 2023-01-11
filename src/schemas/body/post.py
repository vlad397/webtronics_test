from schemas.base import BaseSchema


class PostBodySchema(BaseSchema):
    header: str
    description: str
