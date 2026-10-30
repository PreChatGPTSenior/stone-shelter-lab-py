"""Validated adoption input contracts for shelter ingestion."""

from uuid import UUID

from pydantic import AwareDatetime, Field, field_validator
from pydantic_core import PydanticCustomError

from stone_shelter.adoption.enums import AdoptionStatus, CaseEventType
from stone_shelter.api.contracts import ApiRequest


class CaseEventCreateRequest(ApiRequest):
    external_id: UUID = Field(alias="externalId")
    event_type: CaseEventType = Field(alias="eventType")
    occurred_at: AwareDatetime = Field(alias="occurredAt")
    event_notes: str = Field(min_length=1, alias="eventNotes")


class ShelterCaseCreateRequest(ApiRequest):
    external_id: UUID = Field(alias="externalId")
    case_number: str = Field(min_length=1, alias="caseNumber")
    current_shelter_id: UUID = Field(alias="currentShelterId")
    adoption_status: AdoptionStatus = Field(alias="adoptionStatus")
    admission_date: AwareDatetime = Field(alias="admissionDate")
    events: list[CaseEventCreateRequest] = Field(min_length=1)

    @field_validator("events")
    @classmethod
    def check_event_limit(
        cls,
        events: list[CaseEventCreateRequest],
    ) -> list[CaseEventCreateRequest]:
        limit = 100
        if len(events) > limit:
            raise PydanticCustomError(
                "CASE_EVENT_LIMIT_EXCEEDED",
                "Case history exceeds the limit of {limit} events.",
                {"limit": limit, "actual": len(events)},
            )
        return events

    @field_validator("events")
    @classmethod
    def require_initial_admission(
        cls,
        events: list[CaseEventCreateRequest],
    ) -> list[CaseEventCreateRequest]:
        if not any(event.event_type is CaseEventType.ADMITTED for event in events):
            raise PydanticCustomError(
                "CASE_ADMITTED_EVENT_REQUIRED",
                "Case events must include {required_event_type}.",
                {"required_event_type": CaseEventType.ADMITTED.value},
            )
        return events
