from typing import AsyncGenerator

import config  # type: ignore
from aiohttp import web
from databases import Database


class StorageConfig(config.PostgresConfig):
    @property
    def uri(self) -> str:
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


def create_db_engine(config: StorageConfig):
    async def db_engine(app: web.Application) -> AsyncGenerator[None, None]:
        app["db"] = Database(
            config.uri,
            min_size=config.min_pool_size,
            max_size=config.max_pool_size,
        )

        await app["db"].connect()

        yield

        await app["db"].disconnect()

    return db_engine


def setup(app: web.Application, root: str, config: StorageConfig) -> None:
    app["storage_root"] = root

    app.cleanup_ctx.append(create_db_engine(config))
