import sqlalchemy  # type: ignore
from databases import Database

from aiohttp_storage.storage.abc import Storage


metadata = sqlalchemy.MetaData()


class DBStorage(Storage):
    def __init__(self, database: Database) -> None:
        self._database = database
        self._transaction = None

    async def __aenter__(self):
        self._transaction = await self._database.transaction()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

    async def commit(self):
        await self._transaction.commit()

    async def rollback(self):
        await self._transaction.rollback()
