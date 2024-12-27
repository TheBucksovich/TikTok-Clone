from fastapi import FastAPI
from tik_tok.core.config import settings
from tik_tok.api.routes import health

app = FastAPI(
    title=settings.app_name,
    redoc_url=None,
)

app.include_router(health.router)

