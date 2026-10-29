"""Shared SQLAlchemy declarative base and metadata. Later provide mapping infrastructure without importing business services or owning their repositories."""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(schema="stone_shelter")
