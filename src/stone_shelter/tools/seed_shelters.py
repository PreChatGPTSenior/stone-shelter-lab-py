"""Create missing local reference shelters without overwriting existing records."""

import argparse
import asyncio
import json
from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from stone_shelter.adoption.persistence.models import ShelterModel
from stone_shelter.infrastructure.database import models as orm_models  # noqa: F401
from stone_shelter.infrastructure.database.engine import create_database_engine
from stone_shelter.infrastructure.database.session import create_session_factory
from stone_shelter.settings import DatabaseSettings


async def seed_shelters(sessions: async_sessionmaker[AsyncSession], source: Path) -> int:
    rows: list[dict[str, str]] = json.loads(source.read_text())
    created = 0
    async with sessions() as session, session.begin():
        for row in rows:
            shelter_id = UUID(row["id"])
            existing = await session.get(ShelterModel, shelter_id)
            if existing is not None:
                if existing.name != row["name"] or existing.address != row["address"]:
                    raise ValueError(
                        f"Existing shelter {shelter_id} conflicts with reference data."
                    )
                continue
            session.add(ShelterModel(id=shelter_id, name=row["name"], address=row["address"]))
            created += 1
    return created


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=Path("fixtures/shelters.json"))
    arguments = parser.parse_args()
    engine = create_database_engine(DatabaseSettings())
    try:
        created = await seed_shelters(create_session_factory(engine), arguments.file)
        print(f"Reference shelters ready: {created} created; existing records preserved.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
