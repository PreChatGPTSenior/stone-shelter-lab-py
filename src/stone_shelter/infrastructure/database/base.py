"""Shared SQLAlchemy declarative base and metadata. Later provide mapping infrastructure without importing business services or owning their repositories."""

from uuid import UUID, uuid4

from sqlalchemy import MetaData, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(schema="stone_shelter")

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )