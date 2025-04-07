import uuid
from datetime import datetime
from typing import Optional, List, Any
from asyncpg import Record
from app.schemas.booking import BookingCreate, BookingInDB, BookingUpdate, BookingStatus
from app.database.database import AsyncDatabase


class BookingRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db

    @staticmethod
    def record_to_booking(record: Record) -> BookingInDB:
        """"""
        return BookingInDB(
            client_id=record["client_id"],
            technician_id=record["technician_id"],
            service_type=record["service_type"],
            description=record["description"],
            price=record["price"],
            status=record["status"],
            start_date=record["start_date"],
            end_date=record["end_date"],
            booking_id=record["booking_id"],
            created_at=record["created_at"]
        )
    
    async def get_all_bookings(self) -> List[BookingInDB]:
        """"""
        records = await self.db.fetch("SELECT * FROM bookings")
        return [BookingRepository.record_to_booking(r) for r in records]
    
    async def get_booking_by_id(self, booking_id: str) -> Optional[BookingInDB]:
        """"""
        records = await self.db.fetchrow(
            f"SELECT * FROM bookings WHERE booking_id = $1",
            uuid.UUID(booking_id)
            )
        return [BookingRepository.record_to_booking(r) for r in records]
    
    async def get_bookings_by_client_id(self, client_id: str) -> List[BookingInDB]:
        """"""
        return await self._get_by("client_id", uuid.UUID(client_id))
    
    async def get_bookings_by_technician_id(self, technician_id: str) -> List[BookingInDB]:
        """"""
        return await self._get_by("technician_id", uuid.UUID(technician_id))
    
    async def get_bookings_by_service_type(self, service_type: str) -> List[BookingInDB]:
        """"""
        return await self._get_by("service_type", service_type)
    
    async def get_bookings_by_status(self, status: BookingStatus) -> List[BookingInDB]:
        """"""
        return await self._get_by("status", status.value)
    
    async def _get_by(self, column_name: str, value: Any) -> List[BookingInDB]:
        """"""
        records = await self.db.fetch(
            f"SELECT * FROM bookings WHERE {column_name} = $1",
            value
            )
        return [BookingRepository.record_to_booking(r) for r in records]
    
    async def update_booking(self, booking_id: str, update_data: BookingUpdate) -> BookingInDB:
        """"""
        fields: dict = {
            "description": update_data.description,
            "price": update_data.price,
            "status": update_data.status,
            "start_date": update_data.start_date,
            "end_date": update_data.end_date
        }

        fields = {k: v for k, v in fields.items() if v is not None}
        updates: list = [f"{k} = {i}" for i, k in enumerate(fields.keys(), start=2)]
        values = [uuid.UUID(booking_id), *tuple(fields.values())]

        await self.db.execute(
            f"""
            UPDATE bookings SET {', '.join(updates)}
            WHERE booking_id = $1
            """,
            *values
        )
        return await self.get_booking_by_id(booking_id)
    
    async def delete_booking(self, booking_id: str) -> bool:
        """"""
        result = await self.db.execute("DELETE FROM bookings WHERE booking_id = $1", booking_id)
        return result == "DELETE 0"
    
    async def create(self, booking_data: BookingCreate) -> BookingInDB:
        """"""
        query: str = """
        INSERT INTO bookings
            (client_id, technician_id, service_type, description,
            price, status, start_date, end_date)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING booking_id
        """
        booking_id = await self.db.fetchrow(
            query,
            booking_data.client_id,
            booking_data.technician_id,
            booking_data.service_type,
            booking_data.description,
            booking_data.price,
            booking_data.status,
            booking_data.start_date,
            booking_data.end_date
        )
        return await self.get_booking_by_id(str(booking_id))
