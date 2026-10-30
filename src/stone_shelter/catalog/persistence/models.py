"""Catalog SQLAlchemy mappings. Define tables and relationships for catalog-owned data. Keep transport schemas and adoption lifecycle state separate."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text, Uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from stone_shelter.infrastructure.database.base import Base
from stone_shelter.infrastructure.database.mixins import (
    CreatedAtMixin,
    UpdatedAtMixin,
    VersionedMixin,
)

if TYPE_CHECKING:
    from stone_shelter.adoption.persistence.models import ShelterCaseModel


class StoneModel(CreatedAtMixin, UpdatedAtMixin, VersionedMixin, Base):
    __tablename__ = "stones"

    external_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(120))
    stone_type: Mapped[str] = mapped_column(String(32))
    stone_size: Mapped[str] = mapped_column(String(32))
    biography: Mapped[str | None] = mapped_column(String(2048))
    profile: Mapped["StoneProfileModel | None"] = relationship(
        back_populates="stone",
    )
    shelter_case: Mapped["ShelterCaseModel"] = relationship(
        back_populates="stone",
        lazy="raise",
    )


class StoneProfileModel(CreatedAtMixin, UpdatedAtMixin, VersionedMixin, Base):
    __tablename__ = "stone_profiles"

    stone_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("stones.id"),
        nullable=False,
        unique=True,
    )

    socialization_traits: Mapped[list[str]] = mapped_column(
        ARRAY(String(32)),
        nullable=False,
        default=list,
    )

    care_level: Mapped[str | None] = mapped_column(String(32))
    health_notes: Mapped[str | None] = mapped_column(Text)
    trigger_notes: Mapped[str | None] = mapped_column(Text)
    preferred_environment: Mapped[str | None] = mapped_column(Text)

    stone: Mapped["StoneModel"] = relationship(
        back_populates="profile",
    )
