"""Future stone domain model. Later describe specimen properties and their invariants. Adoption availability belongs to an adoption listing, not to the stone."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4


class StoneType(StrEnum):
    BASALT = "BASALT"
    GRANITE = "GRANITE"
    OBSIDIAN = "OBSIDIAN"
    PUMICE = "PUMICE"
    LIMESTONE = "LIMESTONE"
    SANDSTONE = "SANDSTONE"
    SHALE = "SHALE"
    MARBLE = "MARBLE"
    GNEISS = "GNEISS"
    SLATE = "SLATE"


class StoneSize(StrEnum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


@dataclass
class Stone:
    name: str
    stone_type: StoneType
    stone_size: StoneSize
    admission_date: datetime
    biography: str | None = None
    id: UUID = field(default_factory=uuid4)
