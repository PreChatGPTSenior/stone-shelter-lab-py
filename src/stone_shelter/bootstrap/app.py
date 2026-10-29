"""Application composition and lifecycle. Assemble FastAPI, register routers and error handlers, and manage shared resource startup and shutdown."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from stone_shelter.catalog.api.router import router as catalog_router
from stone_shelter.infrastructure.database.engine import create_database_engine
from stone_shelter.infrastructure.database.session import create_session_factory
from stone_shelter.settings import DatabaseSettings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = create_database_engine(DatabaseSettings())

    try:
        app.state.session_factory = create_session_factory(engine)
        yield
    finally:
        await engine.dispose()


def create_app() -> FastAPI:
    """Build and configure the HTTP application."""
    app = FastAPI(
        title="Stone Shelter API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(catalog_router)

    return app
