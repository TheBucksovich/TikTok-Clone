from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from tik_tok.core.config import settings


def make_pg_options(
    app_name: str = settings.app_name,
    statement_timeout: int = 40_000,
    lock_timeout: int = 30_000,
    idle_in_transaction_session_timeout: int = 60_000,
) -> dict:
    return {
        "application_name": app_name,
        "statement_timeout": str(statement_timeout),
        "lock_timeout": str(lock_timeout),
        "idle_in_transaction_session_timeout": str(idle_in_transaction_session_timeout),
    }


async_engine = create_async_engine(
    settings.db_dsn,
    connect_args={"server_settings": make_pg_options()},
    echo=settings.app_env == "local",
)

async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False
)

async def get_async_session():
    async with async_session() as session:
        yield session