"""Map shelters, lifetime cases, and their life events to database tables."""

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stone_shelter.infrastructure.database.base import Base
from stone_shelter.infrastructure.database.mixins import (
    CreatedAtMixin,
    UpdatedAtMixin,
    VersionedMixin,
)

if TYPE_CHECKING:
    from stone_shelter.catalog.persistence.models import StoneModel


class ShelterModel(CreatedAtMixin, UpdatedAtMixin, VersionedMixin, Base):
    __tablename__ = "shelters"

    name: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(Text)

    cases: Mapped[list["ShelterCaseModel"]] = relationship(
        back_populates="current_shelter",
        lazy="raise",
    )


class ShelterCaseModel(CreatedAtMixin, UpdatedAtMixin, VersionedMixin, Base):
    __tablename__ = "shelter_cases"

    external_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
        unique=True,
    )

    case_number: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    stone_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("stones.id"),
        nullable=False,
        unique=True,
    )

    current_shelter_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("shelters.id"),
        nullable=False,
        index=True,
    )

    adoption_status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    admission_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    stone: Mapped["StoneModel"] = relationship(
        back_populates="shelter_case",
        lazy="raise",
    )

    current_shelter: Mapped["ShelterModel"] = relationship(
        back_populates="cases",
        lazy="raise",
    )

    events: Mapped[list["CaseEventModel"]] = relationship(
        back_populates="case",
        order_by="CaseEventModel.occurred_at",
        lazy="raise",
    )


class CaseEventModel(CreatedAtMixin, Base):
    __tablename__ = "case_events"

    external_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
        unique=True,
    )

    case_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("shelter_cases.id"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    event_notes: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    case: Mapped["ShelterCaseModel"] = relationship(
        back_populates="events",
        lazy="raise",
    )
