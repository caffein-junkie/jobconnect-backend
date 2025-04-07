from pathlib import Path
from typing import Final

import asyncpg
import logging

DATABASE_SCRIPT: Final[Path] = Path(__file__).parent / "jobconnect.sql"
LOGGER = logging.getLogger(__name__)


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
        DROP TABLE IF EXISTS admins CASCADE;
        DROP TABLE IF EXISTS clients CASCADE;
        DROP TABLE IF EXISTS technicians CASCADE;
        DROP TABLE IF EXISTS bookings CASCADE;
        DROP TABLE IF EXISTS ratings CASCADE;
        DROP TABLE IF EXISTS payments CASCADE;
        DROP TABLE IF EXISTS notifications CASCADE;
        DROP TABLE IF EXISTS favorite_technicians CASCADE;
        DROP TABLE IF EXISTS favorite_technicians CASCADE;
        DROP TABLE IF EXISTS technician_availability;
        DROP TABLE IF EXISTS conversations CASCADE;
        DROP TABLE IF EXISTS messages CASCADE;
        DROP TABLE IF EXISTS disputes CASCADE;
        DROP TABLE IF EXISTS dispute_attachments CASCADE;
        DROP TABLE IF EXISTS dispute_comments CASCADE;
        DROP TABLE IF EXISTS password_reset_tokens CASCADE;
        DROP TABLE IF EXISTS technician_service_areas CASCADE;
        DROP TABLE IF EXISTS service_zones CASCADE;
        DROP TABLE IF EXISTS service_categories CASCADE;
        """
        try:
            await self.execute(query)
            LOGGER.info("ALL DATABASE TABLES DROPPED")
            return None
        except Exception as e:
            LOGGER.error(f"COULD NOT DROP TABLES: {e}")
            raise
