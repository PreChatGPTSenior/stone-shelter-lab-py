"""Internal catalog dependency contracts. Later describe the repository operations required by catalog application logic without depending on SQLAlchemy."""

from typing import Protocol

from stone_shelter.catalog.domain.stone import Stone


class StoneRepository(Protocol):
    async def add(self, stone: Stone) -> None: ...
