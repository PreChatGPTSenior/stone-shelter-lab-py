"""Future Alembic migration environment. Later connect migration execution to settings and registered SQLAlchemy metadata. This placeholder does not run migrations."""

import asyncio

from alembic import context
from sqlalchemy.engine import Connection

from stone_shelter.infrastructure.database.base import Base
from stone_shelter.infrastructure.database.engine import create_database_engine
from stone_shelter.settings import DatabaseSettings


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    engine = create_database_engine(DatabaseSettings())

    try:
        async with engine.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await engine.dispose()


asyncio.run(run_async_migrations())
