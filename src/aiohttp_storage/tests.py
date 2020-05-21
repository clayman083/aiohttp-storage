import os
from contextlib import contextmanager
from typing import Generator

from alembic import command  # type: ignore
from alembic.config import Config as AlembicConfig  # type: ignore

from aiohttp_storage import StorageConfig


@contextmanager
def storage(config: StorageConfig, root: str) -> Generator[None, None, None]:
    migrations_root = os.path.join(root, "migrations")
    config_path = os.path.join(migrations_root, "alembic.ini")

    migrations_config = AlembicConfig(config_path)
    migrations_config.set_main_option("script_location", migrations_root)
    migrations_config.set_main_option("sqlalchemy.url", config.uri)

    command.upgrade(migrations_config, "head")

    yield

    command.downgrade(migrations_config, "base")
