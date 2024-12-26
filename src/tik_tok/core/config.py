from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name: str
    project_descr: str
    app_name: str
    app_version: str
    app_env: str
    log_level: str
    timezone: str
    debug: bool

    class Config:
        env_file = ".env"


settings = Settings(
    project_name="TikTok Clone",
    project_descr="TikTok Tape Clone",
    app_name="TikTok Clone",
    app_version="1.0.0",
    app_env="development",
    log_level="INFO",
    timezone="Europe/Moscow",
    debug=True

)
