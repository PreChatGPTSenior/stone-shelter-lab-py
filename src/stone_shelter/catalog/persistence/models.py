"""Catalog SQLAlchemy mappings. Later define tables and relationships for catalog-owned data. Keep transport schemas and adoption lifecycle state separate."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from stone_shelter.infrastructure.database.base import Base


class StoneModel(Base):
    __tablename__ = "stones"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(120))
    stone_type: Mapped[str] = mapped_column(String(32))
    stone_size: Mapped[str] = mapped_column(String(32))
    admission_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    biography: Mapped[str | None] = mapped_column(String(2048))
