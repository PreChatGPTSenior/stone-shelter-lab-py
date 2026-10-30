"""Future stone domain model. Later describe specimen properties and their invariants. Adoption availability belongs to an adoption listing, not to the stone."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4



@dataclass
class Shelter:
    name: str
    address: str
    id: UUID = field(default_factory=uuid4)
ShelterCase