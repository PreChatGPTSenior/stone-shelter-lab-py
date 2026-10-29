from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine

from stone_shelter.bootstrap.app import create_app


def test_lifespan_initializes_and_disposes_database(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Mock()
    settings_class = Mock(return_value=settings)

    engine = AsyncMock(spec=AsyncEngine)
    engine_creator = Mock(return_value=engine)

    session_factory = Mock()
    factory_creator = Mock(return_value=session_factory)

    monkeypatch.setattr(
        "stone_shelter.bootstrap.app.DatabaseSettings",
        settings_class,
    )
    monkeypatch.setattr(
        "stone_shelter.bootstrap.app.create_database_engine",
        engine_creator,
    )
    monkeypatch.setattr(
        "stone_shelter.bootstrap.app.create_session_factory",
        factory_creator,
    )

    app = create_app()

    with TestClient(app):
        settings_class.assert_called_once_with()
        engine_creator.assert_called_once_with(settings)
        factory_creator.assert_called_once_with(engine)
        assert app.state.session_factory is session_factory
        engine.dispose.assert_not_awaited()

    engine.dispose.assert_awaited_once_with()
