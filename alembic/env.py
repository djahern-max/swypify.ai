import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Print the current Python path for debugging
print("Current Python Path:", sys.path)

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print("Updated Python Path:", sys.path)  # Print the updated Python path

from app.models import Base  # Importing models from the app directory
from app.config import settings

# Alembic configuration object
config = context.config

# Set SQLAlchemy URL from the settings
config.set_main_option(
    "sqlalchemy.url",
    f'postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
)


# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for migrations
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine whether to run migrations in online or offline mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
