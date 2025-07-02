import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Garante que a pasta raiz (onde está app/) esteja no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# importa seu metadata
from app.models import Base

# carrega config do alembic.ini
config = context.config
fileConfig(config.config_file_name)

# Sobrescreve a URL padrão pelo valor da variável de ambiente
db_url = os.getenv('DATABASE_URL')
if not db_url:
    raise RuntimeError("Você precisa definir a variável de ambiente DATABASE_URL")
config.set_main_option('sqlalchemy.url', db_url)

# metadata dos modelos (para autogenerate)
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
