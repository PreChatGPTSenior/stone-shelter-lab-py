"""Repository operations used by catalog application scenarios."""

from typing import Protocol

from stone_shelter.catalog.persistence.models import StoneModel


class StoneRepository(Protocol):
    def add(self, stone: StoneModel) -> None: ...
