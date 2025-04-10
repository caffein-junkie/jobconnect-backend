from pathlib import Path
from typing import Final

import asyncpg
import logging

LOGGER = logging.getLogger(__name__)

BASE_PATH: Final[Path] = Path(__file__).parent
DATABASE_SCRIPT: Final[Path] = BASE_PATH / "jobconnect.sql"
DUMMY_DATA_SCRIPT: Final[Path] = BASE_PATH / "dummy_data.sql"


class AsyncDatabase:

    def __init__(
        self,
        host: str,
        dbname: str,
        username: str,
        password: str,
        port: int = 5432
    ) -> None:
        self._host: str = host
        self._dbname: str = dbname
        self._username: str = username
        self._password: str = password
        self._port: int = port
        self._connection_pool = None
    
    async def connect(self) -> None:
        """"""
        if not self._connection_pool:
            self._connection_pool = await asyncpg.create_pool(
                host=self._host,
                database=self._dbname,
                user=self._username,
                password=self._password,
                port=self._port,
                min_size=1,
                max_size=10
            )
            LOGGER.info("CONNECTED TO THE DATABASE SUCCESSFULLY")

    async def disconnect(self) -> None:
        """"""
        if self._connection_pool:
            await self._connection_pool.close()
            LOGGER.info("DISCONNECTED FROM THE DATABASE SUCCESSFULLY")
    
    async def execute(self, query: str, *args):
        """"""
        async with self._connection_pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args):
        """"""
        async with self._connection_pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def fetchrow(self, query: str, *args):
        """"""
        async with self._connection_pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    
    async def initdb(self) -> None:
        """"""
        try:
            sql: str = DATABASE_SCRIPT.read_text()
            async with self._connection_pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(sql)
            
            LOGGER.info("CREATED DATABASE SCHEMA SUCCESSFULLY")
        except asyncpg.exceptions.DuplicateTableError:
            LOGGER.info("DATABASE ALREADY INITIALIZED - SKIPPING TABLE CREATION.")
        except Exception as e:
            LOGGER.error(f"ERROR CREATING DATABASE: {repr(e)}")

    async def drop_tables(self) -> None:
        """"""
        query = """
        DROP TABLE IF EXISTS admin CASCADE;
        DROP TABLE IF EXISTS client CASCADE;
        DROP TABLE IF EXISTS technician CASCADE;
        DROP TABLE IF EXISTS booking CASCADE;
        DROP TABLE IF EXISTS rating CASCADE;
        DROP TABLE IF EXISTS payment CASCADE;
        DROP TABLE IF EXISTS notification CASCADE;
        DROP TABLE IF EXISTS favorite_technician CASCADE;
        """
        try:
            await self.execute(query)
            LOGGER.info("ALL DATABASE TABLES DROPPED")
            return None
        except Exception as e:
            LOGGER.error(f"COULD NOT DROP TABLES: {e}")
            raise

    async def populate_with_dummy_data(self) -> None:
        """"""
        try:
            sql: str = DUMMY_DATA_SCRIPT.read_text()
            await self.execute(sql)
            LOGGER.info("SUCCESSFULLY CREATED THE DUMMY DATA")
        except Exception as e:
            LOGGER.error(f"FAILED TO CREATE DUMMY DATA: {e}")
