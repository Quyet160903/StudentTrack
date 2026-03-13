"""fix nullable constraints

Revision ID: 624c731ff05d
Revises: 9477e9020be2
Create Date: 2026-03-09 17:14:57.189071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '624c731ff05d'
down_revision: Union[str, Sequence[str], None] = '9477e9020be2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('application_status_logs', 'old_status',
               existing_type=postgresql.ENUM('PENDING', 'REVIEWING', 'INTERVIEW', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='applicationstatus'),
               nullable=True)
    op.alter_column('application_status_logs', 'note', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('applications', 'cover_letter', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('applications', 'resume_url', existing_type=sa.VARCHAR(length=500), nullable=True)
    op.alter_column('companies', 'description', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('companies', 'website', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column('companies', 'location', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column('companies', 'contact_phone', existing_type=sa.VARCHAR(length=20), nullable=True)
    op.alter_column('companies', 'logo_url', existing_type=sa.VARCHAR(length=500), nullable=True)
    op.alter_column('coordinators', 'department', existing_type=sa.VARCHAR(length=100), nullable=True)
    op.alter_column('coordinators', 'phone', existing_type=sa.VARCHAR(length=20), nullable=True)
    op.alter_column('job_postings', 'description', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('job_postings', 'requirements', existing_type=sa.TEXT(), nullable=True)
    op.alter_column('job_postings', 'location', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column('job_postings', 'salary_min', existing_type=sa.NUMERIC(precision=10, scale=2), nullable=True)
    op.alter_column('job_postings', 'salary_max', existing_type=sa.NUMERIC(precision=10, scale=2), nullable=True)
    op.alter_column('job_postings', 'deadline', existing_type=postgresql.TIMESTAMP(), nullable=True)
    op.alter_column('students', 'major', existing_type=sa.VARCHAR(length=100), nullable=True)
    op.alter_column('students', 'gpa', existing_type=sa.DOUBLE_PRECISION(precision=53), nullable=True)
    op.alter_column('students', 'phone', existing_type=sa.VARCHAR(length=20), nullable=True)
    op.alter_column('students', 'graduation_year', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('students', 'resume_url', existing_type=sa.VARCHAR(length=500), nullable=True)
    op.alter_column('students', 'bio', existing_type=sa.TEXT(), nullable=True)
    op.create_unique_constraint('users_email_key', 'users', ['email'])  # FIXED


def downgrade() -> None:
    op.drop_constraint('users_email_key', 'users', type_='unique')  # FIXED
    op.alter_column('students', 'bio', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('students', 'resume_url', existing_type=sa.VARCHAR(length=500), nullable=False)
    op.alter_column('students', 'graduation_year', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('students', 'phone', existing_type=sa.VARCHAR(length=20), nullable=False)
    op.alter_column('students', 'gpa', existing_type=sa.DOUBLE_PRECISION(precision=53), nullable=False)
    op.alter_column('students', 'major', existing_type=sa.VARCHAR(length=100), nullable=False)
    op.alter_column('job_postings', 'deadline', existing_type=postgresql.TIMESTAMP(), nullable=False)
    op.alter_column('job_postings', 'salary_max', existing_type=sa.NUMERIC(precision=10, scale=2), nullable=False)
    op.alter_column('job_postings', 'salary_min', existing_type=sa.NUMERIC(precision=10, scale=2), nullable=False)
    op.alter_column('job_postings', 'location', existing_type=sa.VARCHAR(length=255), nullable=False)
    op.alter_column('job_postings', 'requirements', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('job_postings', 'description', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('coordinators', 'phone', existing_type=sa.VARCHAR(length=20), nullable=False)
    op.alter_column('coordinators', 'department', existing_type=sa.VARCHAR(length=100), nullable=False)
    op.alter_column('companies', 'logo_url', existing_type=sa.VARCHAR(length=500), nullable=False)
    op.alter_column('companies', 'contact_phone', existing_type=sa.VARCHAR(length=20), nullable=False)
    op.alter_column('companies', 'location', existing_type=sa.VARCHAR(length=255), nullable=False)
    op.alter_column('companies', 'website', existing_type=sa.VARCHAR(length=255), nullable=False)
    op.alter_column('companies', 'description', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('applications', 'resume_url', existing_type=sa.VARCHAR(length=500), nullable=False)
    op.alter_column('applications', 'cover_letter', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('application_status_logs', 'note', existing_type=sa.TEXT(), nullable=False)
    op.alter_column('application_status_logs', 'old_status',
               existing_type=postgresql.ENUM('PENDING', 'REVIEWING', 'INTERVIEW', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='applicationstatus'),
               nullable=False)