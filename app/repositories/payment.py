import uuid
from typing import Any, Optional, List
from app.schemas.payment import PaymentCreate, PaymentInDB, PaymentUpdate, PaymentStatus, PaymentMethod
from app.database.database import AsyncDatabase
from asyncpg import Record


class PaymentRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db

    @staticmethod
    def record_to_payment(record: Record) -> PaymentInDB:
        """"""
        return PaymentInDB(
            booking_id=str(record["booking_id"]),
            client_id=str(record["client_id"]),
            technician_id=str(record["technician_id"]),
            amount=record["amount"],
            payment_method=record["payment_method"],
            payment_status=record["payment_status"],
            payment_id=str(record["payment_id"]),
            transaction_date=record["transaction_date"]
        )
    
    async def get_all_payments(self) -> List[PaymentInDB]:
        """"""
        records = await self.db.fetch("SELECT * FROM payment")
        return [PaymentRepository.record_to_payment(p) for p in records]
    
    async def get_payment_by_id(self, payment_id: str) -> Optional[PaymentInDB]:
        """"""
        record = await self.db.fetchrow(
            "SELECT * FROM payment WHERE payment_id = $1", uuid.UUID(payment_id)
            )
        return PaymentRepository.record_to_payment(record) if record is not None else None
    
    async def get_all_payments_by_technician_id(self, technician_id: str) -> List[PaymentInDB]:
        """"""
        return await self._get_all_by("technician_id", uuid.UUID(technician_id))
    
    async def get_all_payments_by_client_id(self, client_id: str) -> List[PaymentInDB]:
        """"""
        return await self._get_all_by("client_id", uuid.UUID(client_id))
    
    async def get_all_payments_by_booking_id(self, booking_id: str) -> List[PaymentInDB]:
        """"""
        return await self._get_all_by("booking_id", uuid.UUID(booking_id))
    
    async def get_all_payments_by_payment_status(self, status: PaymentStatus) -> List[PaymentInDB]:
        """"""
        return await self._get_all_by("payment_status", status)
    
    async def get_all_payments_by_payment_method(self, method: PaymentMethod) -> List[PaymentInDB]:
        """"""
        return await self._get_all_by("payment_method", method)
    
    async def _get_all_by(self, column_name: str, value: Any) -> List[PaymentInDB]:
        """"""
        records = await self.db.fetch(f"SELECT * FROM payment WHERE {column_name} = $1", value)
        return [PaymentRepository.record_to_payment(p) for p in records]
    
    async def create(self, payment_data: PaymentCreate) -> PaymentInDB:
        """"""
        id = await self.db.fetchrow(
            """
            INSERT INTO payment (
                booking_id, technician_id, client_id, amount, payment_method,
                payment_status
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING payment_id
            """,
            payment_data.booking_id,
            payment_data.technician_id,
            payment_data.client_id,
            payment_data.amount,
            payment_data.payment_method,
            payment_data.payment_status,
        )
        return await self.get_payment_by_id(id)
    
    async def update(self, payment_id: str, update_data: PaymentUpdate) -> PaymentInDB:
        """"""
        fields: dict = {
            "amount": update_data.amount,
            "payment_method": update_data.payment_method,
            "payment_status": update_data.payment_status
        }

        fields = {k: v for k, v in fields.items() if v is not None}

        if len(fields) == 0: return await self.get_payment_by_id(payment_id)

        updates: list = [f"{k} = ${i}" for i, k in enumerate(fields.keys(), start=2)]
        values: list = [uuid.UUID(payment_id), *tuple(fields.values())]

        query: str = f"""
        UPDATE payment SET {', '.join(updates)}
        WHERE payment_id = $1
        """

        await self.db.execute(query, *values)
        return self.get_payment_by_id(payment_id)
    
    async def delete(self, payment_id: str) -> bool:
        """"""
        await self.db.execute("DELETE FROM payment WHERE payment_id = $1", uuid.UUID(payment_id))
