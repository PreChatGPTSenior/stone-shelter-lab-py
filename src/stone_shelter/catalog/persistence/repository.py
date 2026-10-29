"""Catalog persistence adapter. Later implement repository ports using an injected session. Flush when needed, but leave commit and rollback to the Unit of Work."""

from sqlalchemy.ext.asyncio import AsyncSession

from stone_shelter.catalog.domain.stone import Stone
from stone_shelter.catalog.persistence.models import StoneModel


class SqlAlchemyStoneRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, stone: Stone) -> None:
        model = StoneModel(
            id=stone.id,
            name=stone.name,
            stone_type=stone.stone_type.value,
            stone_size=stone.stone_size.value,
            admission_date=stone.admission_date,
            biography=stone.biography,
        )

        self._session.add(model)
        await self._session.flush()
