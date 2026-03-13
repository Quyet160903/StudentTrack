"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'pending'")
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'approved'")
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'rejected'")

    op.add_column('job_postings', sa.Column('rejection_note', sa.String(), nullable=True))
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('job_postings', 'rejection_note')
    ${downgrades if downgrades else "pass"}
