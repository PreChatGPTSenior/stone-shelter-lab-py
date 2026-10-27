"""Application composition and lifecycle. Assemble FastAPI, register routers and error handlers, and manage shared resource startup and shutdown."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Build and configure the HTTP application."""
    app = FastAPI(
        title="Stone Shelter API",
        version="0.1.0",
    )

    return app