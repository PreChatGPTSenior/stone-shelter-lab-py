from collections.abc import AsyncIterator
from datetime import UTC, datetime
from uuid import UUID, uuid4

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from stone_shelter.bootstrap.app import create_app
from stone_shelter.catalog.persistence.models import StoneModel


@pytest_asyncio.fixture
async def app() -> AsyncIterator[FastAPI]:
    application = create_app()

    async with application.router.lifespan_context(application):
        yield application


@pytest.mark.asyncio
async def test_create_stone_persists_validated_data(app: FastAPI) -> None:
    session_factory: async_sessionmaker[AsyncSession] = app.state.session_factory
    name = f"Meadow-{uuid4().hex}"
    supplied_id = uuid4()
    started_at = datetime.now(UTC)

    payload = {
        "name": f"  {name}  ",
        "stoneType": "GRANITE",
        "stoneSize": "SMALL",
        "biography": "  A quiet companion.  ",
        "id": str(supplied_id),
        "admissionDate": "2000-01-01T00:00:00Z",
        "adoptionStatus": "ADOPTED",
    }

    try:
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.post("/api/v1/stones", json=payload)

        finished_at = datetime.now(UTC)

        assert response.status_code == 201, response.text
        body = response.json()
        assert set(body) == {"id"}

        created_id = UUID(body["id"])
        assert created_id.version == 4
        assert created_id != supplied_id

        async with session_factory() as session:
            result = await session.execute(select(StoneModel).where(StoneModel.name == name))
            stones = result.scalars().all()

            assert len(stones) == 1
            stone = stones[0]
            assert stone.id == created_id
            assert stone.stone_type == "GRANITE"
            assert stone.stone_size == "SMALL"
            assert stone.biography == "A quiet companion."
            assert started_at <= stone.admission_date <= finished_at
    finally:
        async with session_factory() as session:
            await session.execute(
                delete(StoneModel).where(StoneModel.name.in_([name, f"  {name}  "]))
            )
            await session.commit()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("field", "value"),
    [
        pytest.param("name", "   ", id="blank-name"),
        pytest.param("name", "x" * 121, id="name-too-long"),
        pytest.param("stoneType", "UNKNOWN", id="unknown-type"),
        pytest.param("stoneSize", "HUGE", id="unknown-size"),
        pytest.param("biography", "x" * 2049, id="biography-too-long"),
    ],
)
async def test_create_stone_rejects_invalid_data(
    app: FastAPI,
    field: str,
    value: str,
) -> None:
    session_factory: async_sessionmaker[AsyncSession] = app.state.session_factory
    marker = uuid4().hex
    name = f"Invalid-test-{marker}"
    biography = f"Test biography {marker}"

    payload = {
        "name": name,
        "stoneType": "GRANITE",
        "stoneSize": "SMALL",
        "biography": biography,
        field: value,
    }

    test_row_filter = or_(
        StoneModel.name == name,
        StoneModel.biography == biography,
    )

    try:
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.post("/api/v1/stones", json=payload)

        assert response.status_code == 422, response.text
        assert any(error["loc"] == ["body", field] for error in response.json()["detail"])

        async with session_factory() as session:
            result = await session.execute(select(StoneModel.id).where(test_row_filter))
            assert result.scalars().all() == []
    finally:
        async with session_factory() as session:
            await session.execute(delete(StoneModel).where(test_row_filter))
            await session.commit()
