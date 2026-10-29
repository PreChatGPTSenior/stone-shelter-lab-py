"""Validated catalog input contracts shared by API and application services."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from stone_shelter.catalog.domain.stone import StoneSize, StoneType


class ApiRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
        validate_by_name=True,
        validate_by_alias=True,
    )


class ApiResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        serialize_by_alias=True,
    )


class StoneCreateRequest(ApiRequest):
    name: str = Field(min_length=1, max_length=120)
    stone_type: StoneType = Field(alias="stoneType")
    stone_size: StoneSize = Field(alias="stoneSize")
    biography: str | None = Field(default=None, max_length=2048)


class StoneCreateResponse(ApiResponse):
    id: UUID
