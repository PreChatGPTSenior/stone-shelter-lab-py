"""Load ORM models so their tables are registered in shared metadata."""

from stone_shelter.adoption.persistence import models as adoption_models  # noqa: F401
from stone_shelter.catalog.persistence import models as catalog_models  # noqa: F401
