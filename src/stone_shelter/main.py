"""HTTP application entry point. Expose the application assembled by bootstrap for Uvicorn. Keep business logic out of this module."""

from stone_shelter.bootstrap.app import create_app

app = create_app()
