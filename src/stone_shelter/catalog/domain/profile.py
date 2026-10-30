"""Future stone domain model. Later describe specimen properties and their invariants. Adoption availability belongs to an adoption listing, not to the stone."""

from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4


class CareLevel(StrEnum):
    STANDARD = "STANDARD"
    ADDITIONAL = "ADDITIONAL"
    INTENSIVE = "INTENSIVE"

class SocializationTrait(StrEnum):
    PREFERS_SOLITUDE = "PREFERS_SOLITUDE"
    ENJOYS_HUMAN_COMPANY = "ENJOYS_HUMAN_COMPANY"
    ENJOYS_OTHER_STONES = "ENJOYS_OTHER_STONES"
    GOOD_WITH_CHILDREN = "GOOD_WITH_CHILDREN"
    CAUTIOUS_WITH_STRANGERS = "CAUTIOUS_WITH_STRANGERS"
    NEEDS_SLOW_INTRODUCTION = "NEEDS_SLOW_INTRODUCTION"


@dataclass
class StoneProfile:
    stone_id: UUID
    health_notes: str | None = None
    trigger_notes: str | None = None
    preferred_environment: str | None = None
    care_level: CareLevel | None = None
    id: UUID = field(default_factory=uuid4)
    socialization_traits: set[SocializationTrait] = field(
        default_factory=set,
    )


