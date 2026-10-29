import pytest
from sqlalchemy import text

from stone_shelter.infrastructure.database.engine import create_database_engine
from stone_shelter.infrastructure.database.session import create_session_factory
from stone_shelter.settings import DatabaseSettings


@pytest.mark.asyncio
async def test_application_db_engine() -> None:
    settings = DatabaseSettings()
    engine = create_database_engine(settings)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    finally:
        await engine.dispose()


@pytest.mark.asyncio
async def test_create_session_factory() -> None:
    settings = DatabaseSettings()
    engine = create_database_engine(settings)
    session_factory = create_session_factory(engine)
    try:
        async with session_factory() as session:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    finally:
        await engine.dispose()
