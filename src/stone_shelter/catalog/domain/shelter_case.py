"""Future stone domain model. Later describe specimen properties and their invariants. Adoption availability belongs to an adoption listing, not to the stone."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4


class AdoptionStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    ADOPTED = "ADOPTED"
    RETURNED = "RETURNED"


@dataclass
class ShelterCase:
    name: str
    case_number: str
    external_id: UUID
    stone_id: UUID
    current_shelter_id: UUID
    adoption_status: AdoptionStatus
    admission_date: datetime
    biography: str | None = None
    id: UUID = field(default_factory=uuid4)
