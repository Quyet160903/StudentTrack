from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ── import Base and all models ──
from app.db.database import Base
from app.models.user import User
from app.models.student import Student
from app.models.company import Company
from app.models.coordinator import Coordinator
from app.models.job_posting import JobPosting
from app.models.application import Application
from app.models.application_log import ApplicationStatusLog
from app.models.refresh_token import RefreshToken

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  # ← this is the key line


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()