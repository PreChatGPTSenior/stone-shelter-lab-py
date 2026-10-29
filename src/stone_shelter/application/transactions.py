"""Framework-independent Unit of Work contract. Describe transaction entry, explicit commit, rollback and cleanup responsibilities without importing SQLAlchemy or business modules."""

from types import TracebackType
from typing import Protocol, Self


class UnitOfWork(Protocol):
    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
