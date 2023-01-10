from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import v1
from core.config import config
from db.db import init_db

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api/docs.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    init_db()


app.include_router(v1.router, prefix="/api", tags=["user"])
