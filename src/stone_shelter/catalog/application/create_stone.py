"""Create a stone and explicitly commit the current Unit of Work."""

from datetime import UTC, datetime

from stone_shelter.application.transactions import UnitOfWork
from stone_shelter.catalog.application.ports import StoneRepository
from stone_shelter.catalog.contracts import StoneCreateRequest
from stone_shelter.catalog.domain.stone import Stone


class CreateStoneService:
    def __init__(
        self,
        repository: StoneRepository,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def create(self, request: StoneCreateRequest) -> Stone:
        stone = Stone(
            **request.model_dump(),
            admission_date=datetime.now(UTC),
        )

        await self._repository.add(stone)
        await self._uow.commit()

        return stone
