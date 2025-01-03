from dynaconf import Dynaconf
from pydantic import AnyUrl
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

_settings = Dynaconf(
    settings_files=["config.yaml", ".env"],
)
load_dotenv(".env")

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
    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str
    rabbitmq_url: str

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings(
    app_name="TikTok Clone",
    app_env=_settings.get("app_env", "dev"),
    db_dsn=str(_db_dsn),
    secret_key=_settings.get(
        "SECRET_KEY", "BMUJVZQZUClKl1RYbD9pcrO-Dcaby0DTjr8FdmJdhxI"
    ),
    access_token_expire_minutes=int(_settings.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30)),
    algorithm=_settings.get("ALGORITHM", "HS256"),
    s3_endpoint=_settings.get("S3_ENDPOINT_URL", "http://0.0.0.0:9001"),
    s3_access_key=_settings.get("MINIO_ROOT_USER", "minioadmin"),
    s3_secret_key=_settings.get("MINIO_ROOT_PASSWORD", "minioadmin"),
    s3_bucket_name=_settings.get("S3_BUCKET_NAME", "videos"),
    rabbitmq_url=_settings.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
)
