import uuid
from typing import Optional, List
from asyncpg import Record
from app.database.database import AsyncDatabase
from app.schemas.favorite_technician import (
    FavoriteTechnicianCreate,
    FavoriteTechnicianInDB,
    FavoriteTechnicianResponse
)
from app.utils.exceptions import NotFoundException, DuplicateEntryException


class FavoriteTechnicianRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db

    @staticmethod
    def record_to_favorite_technician(record: Record) -> FavoriteTechnicianInDB:
        """"""
        return FavoriteTechnicianInDB(
            client_id=str(record["client_id"]),
            technician_id=str(record["technician_id"]),
            favorite_id=str(record["id"]),
            created_at=record["created_at"]
        )
    
    async def get_all_favorite_technicians(self) -> List[FavoriteTechnicianInDB]:
        """"""
        records = await self.db.fetch("SELECT * FROM favorite_technician")
        return [FavoriteTechnicianRepository.record_to_favorite_technician(ft) for ft in records]
    
    async def get_favorite_technicians_by_client_id(self, client_id: str) -> List[FavoriteTechnicianInDB]:
        """"""
        records = await self.db.fetch(
            "SELECT * FROM favorite_technician WHERE client_id = $1",
            uuid.UUID(client_id)
            )
        return [FavoriteTechnicianRepository.record_to_favorite_technician(ft) for ft in records]
    
    async def delete(self, client_id: str, technician_id: str) -> None:
        """"""
        await self.db.execute(
            "DELETE FROM favorite_technician WHERE client_id = $1 AND technician_id = $2",
            uuid.UUID(client_id), uuid.UUID(technician_id)
            )
    
    async def create(self, ft_data: FavoriteTechnicianCreate) -> FavoriteTechnicianInDB:
        try:
            await self.db.execute(
                """
                INSERT INTO favorite_technician (client_id, technician_id),
                VALUES ($1, $2)
                """,
                ft_data.client_id,
                ft_data.technician_id
                )
            return self.get_favorite_technicians_by_client_id(ft_data.client_id)
        except DuplicateEntryException:
            raise DuplicateEntryException("Favorite technician already exists.")
