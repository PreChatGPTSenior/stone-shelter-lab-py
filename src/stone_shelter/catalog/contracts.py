"""Validated catalog input contracts shared by API and application services."""

from uuid import UUID

from pydantic import Field

from stone_shelter.api.contracts import ApiRequest, ApiResponse
from stone_shelter.catalog.enums import CareLevel, SocializationTrait, StoneSize, StoneType


class StoneCreateRequest(ApiRequest):
    name: str = Field(min_length=1, max_length=120)
    stone_type: StoneType = Field(alias="stoneType")
    stone_size: StoneSize = Field(alias="stoneSize")
    biography: str | None = Field(default=None, max_length=2048)
    external_id: UUID = Field(alias="externalId")


class StoneProfileCreateRequest(ApiRequest):
    socialization_traits: set[SocializationTrait] = Field(
        default_factory=set,
        alias="socializationTraits",
    )
    care_level: CareLevel | None = Field(default=None, alias="careLevel")
    health_notes: str | None = Field(default=None, alias="healthNotes")
    trigger_notes: str | None = Field(default=None, alias="triggerNotes")
    preferred_environment: str | None = Field(default=None, alias="preferredEnvironment")
