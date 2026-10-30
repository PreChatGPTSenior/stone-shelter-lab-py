"""Input contract for registering one stone with its case and optional profile."""

from uuid import UUID

from pydantic import Field

from stone_shelter.adoption.contracts import ShelterCaseCreateRequest
from stone_shelter.api.contracts import ApiRequest, ApiResponse
from stone_shelter.catalog.contracts import StoneCreateRequest, StoneProfileCreateRequest


class StoneRegistrationRequest(ApiRequest):
    stone: StoneCreateRequest
    shelter_case: ShelterCaseCreateRequest = Field(alias="shelterCase")
    profile: StoneProfileCreateRequest | None = None


class StoneRegistrationResponse(ApiResponse):
    id: UUID
