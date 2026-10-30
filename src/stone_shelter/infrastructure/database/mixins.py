"""Reusable ORM columns for timestamps and optimistic version checks."""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class VersionedMixin:
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    @declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:
        return {
            "version_id_col": cls.version,
        }
