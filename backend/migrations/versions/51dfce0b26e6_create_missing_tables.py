"""create missing tables

Revision ID: 51dfce0b26e6
Revises: abc123
Create Date: 2026-03-13 08:49:48.804839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '51dfce0b26e6'
down_revision: Union[str, Sequence[str], None] = 'abc123'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add enum values safely (ignore if already exists)
    op.execute("""
        DO $$ BEGIN
            ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'pending';
        EXCEPTION WHEN others THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'approved';
        EXCEPTION WHEN others THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            ALTER TYPE jobstatus ADD VALUE IF NOT EXISTS 'rejected';
        EXCEPTION WHEN others THEN null;
        END $$;
    """)

    # Add columns only if they don't exist
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE job_postings ADD COLUMN rejection_note VARCHAR;
        EXCEPTION WHEN duplicate_column THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE job_postings ADD COLUMN job_type jobtype NOT NULL DEFAULT 'internship';
        EXCEPTION WHEN duplicate_column THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE job_postings ADD COLUMN status jobstatus NOT NULL DEFAULT 'pending';
        EXCEPTION WHEN duplicate_column THEN null;
        END $$;
    """)

    op.alter_column('companies', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('coordinators', 'full_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE job_postings DROP COLUMN IF EXISTS rejection_note;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE job_postings DROP COLUMN IF EXISTS status;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            ALTER TABLE job_postings DROP COLUMN IF EXISTS job_type;
        END $$;
    """)
    op.alter_column('coordinators', 'full_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('companies', 'name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)