"""add approval flow"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "abc123"
down_revision = "9c3851f8ac6a"   # migration trước đó
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'pending'")
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'approved'")
    op.execute("ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'rejected'")

    op.add_column(
        "job_postings",
        sa.Column("rejection_note", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("job_postings", "rejection_note")