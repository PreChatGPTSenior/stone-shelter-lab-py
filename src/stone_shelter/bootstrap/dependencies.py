"""Dependency wiring for use cases. Later create a session per execution and bind the Unit of Work and participating module adapters to that same session. Keep business decisions in use cases."""

from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from stone_shelter.catalog.application.create_stone import CreateStoneService
from stone_shelter.catalog.persistence.repository import SqlAlchemyStoneRepository
from stone_shelter.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork


async def get_create_stone_service(
    request: Request,
) -> AsyncIterator[CreateStoneService]:
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory

    uow = SqlAlchemyUnitOfWork(session_factory)

    async with uow:
        repository = SqlAlchemyStoneRepository(uow.session)
        service = CreateStoneService(
            repository=repository,
            uow=uow,
        )

        yield service
