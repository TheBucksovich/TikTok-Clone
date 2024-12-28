from dynaconf import Dynaconf
from pydantic import AnyUrl
from pydantic_settings import BaseSettings

_settings = Dynaconf(
    settings_files=["config.yaml", ".env"],
)

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
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str


settings = Settings(
    app_name="TikTok Clone",
    app_env=_settings.get("app_env", "dev"),
    db_dsn=str(_db_dsn),
    secret_key=_settings.get(
        "SECRET_KEY", "BMUJVZQZUClKl1RYbD9pcrO-Dcaby0DTjr8FdmJdhxI"
    ),
    access_token_expire_minutes=int(_settings.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)),
    algorithm=_settings.get("ALGORITHM", "HS256"),
)
