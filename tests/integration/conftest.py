"""Shared fixtures for isolated PostgreSQL integration tests."""

import os
import subprocess
import sys
from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import pytest_asyncio
from fastapi import FastAPI
from pydantic import SecretStr
from testcontainers.community.postgres import PostgresContainer

from stone_shelter.bootstrap.app import create_app
from stone_shelter.settings import DatabaseSettings

POSTGRES_IMAGE = (
    "pgvector/pgvector:0.8.6-pg18-trixie"
    "@sha256:78bf48b801e792f99e3ac62b5036fd3876e9be48afda16c1e331af1c75ceb2ff"
)


@pytest.fixture(scope="session")
def postgres_container() -> Iterator[PostgresContainer]:
    with PostgresContainer(
        image=POSTGRES_IMAGE,
        username="integration_test",
        password="integration_test",
        dbname="stone_shelter_test",
        driver=None,
    ) as postgres:
        yield postgres


@pytest.fixture(scope="session")
def database_settings(
    postgres_container: PostgresContainer,
) -> DatabaseSettings:
    return DatabaseSettings(
        _env_file=None,
        host=postgres_container.get_container_host_ip(),
        port=int(postgres_container.get_exposed_port(5432)),
        db=postgres_container.dbname,
        user=postgres_container.username,
        password=SecretStr(postgres_container.password),
    )


@pytest.fixture(scope="session")
def migrated_database(
    database_settings: DatabaseSettings,
) -> DatabaseSettings:
    project_root = Path(__file__).resolve().parents[2]

    environment = os.environ.copy()
    environment.update(
        {
            "POSTGRES_HOST": database_settings.host,
            "POSTGRES_PORT": str(database_settings.port),
            "POSTGRES_DB": database_settings.db,
            "POSTGRES_USER": database_settings.user,
            "POSTGRES_PASSWORD": (database_settings.password.get_secret_value()),
        }
    )

    with TemporaryDirectory(prefix="stone-shelter-migrations-") as working_directory:
        for arguments in (("upgrade", "head"), ("check",)):
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "alembic",
                    "-c",
                    str(project_root / "alembic.ini"),
                    *arguments,
                ],
                cwd=working_directory,
                env=environment,
                check=True,
            )

    return database_settings


@pytest_asyncio.fixture
async def app(
    migrated_database: DatabaseSettings,
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncIterator[FastAPI]:
    monkeypatch.setattr(
        "stone_shelter.bootstrap.app.DatabaseSettings",
        lambda: migrated_database,
    )

    application = create_app()

    async with application.router.lifespan_context(application):
        yield application
