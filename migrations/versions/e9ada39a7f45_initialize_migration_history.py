"""Initialize migration history

Revision ID: e9ada39a7f45
Revises:
Create Date: 2026-10-29 10:51:22.402398

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "e9ada39a7f45"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
