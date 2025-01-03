from fastapi import FastAPI
from tik_tok.core.config import settings
from tik_tok.api.routes import users
from tik_tok.api.routes import videos
from tik_tok.core.logging import setup_logging
from prometheus_fastapi_instrumentator import Instrumentator

from tik_tok.core.middleware import LogRequestMiddleware

setup_logging()

app = FastAPI(
    title=settings.app_name,
    redoc_url=None,
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(videos.router, prefix="/videos", tags=["Videos"])


app.add_middleware(LogRequestMiddleware)
Instrumentator().instrument(app).expose(app)
