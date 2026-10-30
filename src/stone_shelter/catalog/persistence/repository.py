"""Register catalog objects in the current session without committing."""

from sqlalchemy.ext.asyncio import AsyncSession

from stone_shelter.catalog.persistence.models import StoneModel


class SqlAlchemyStoneRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add(self, stone: StoneModel) -> None:
        self._session.add(stone)
