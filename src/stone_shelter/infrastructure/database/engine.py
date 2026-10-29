"""Database engine lifecycle. Configure the SQLAlchemy engine and connection pool. Do not open connections as an import side effect."""

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from stone_shelter.settings import DatabaseSettings


def create_database_engine(settings: DatabaseSettings) -> AsyncEngine:
    engine = create_async_engine(
        URL.create(
            drivername="postgresql+asyncpg",
            username=settings.user,
            password=settings.password.get_secret_value(),
            host=settings.host,
            port=settings.port,
            database=settings.db,
        )
    )
    return engine
