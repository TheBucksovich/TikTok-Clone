from zoneinfo import ZoneInfo

from dynaconf import Dynaconf
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

_settings = Dynaconf(settings_files=["config.yaml", ".env"])

_db_dsn = AnyUrl.build(
    scheme="postgresql+asyncpg",
    username=_settings.database.user,
    password=_settings.database.password,
    host=_settings.database.host,
    port=_settings.database.port,
    path=_settings.database.db,
)


class Settings(BaseSettings):
    app_name: str
    app_env: str
    db_dsn: str


settings = Settings(
    app_name="TikTok Clone",
    app_env=_settings.app_env,
    db_dsn=str(_db_dsn),
)