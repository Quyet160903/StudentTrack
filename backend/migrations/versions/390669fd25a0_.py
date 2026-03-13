"""empty message

Revision ID: 390669fd25a0
Revises: 624c731ff05d
Create Date: 2026-03-10 18:03:12.411533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '390669fd25a0'
down_revision: Union[str, Sequence[str], None] = '624c731ff05d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
