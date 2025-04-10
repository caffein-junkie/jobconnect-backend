import uuid
from typing import List, Optional, Any
from app.database.database import AsyncDatabase
from app.schemas.review import ReviewCreate, ReviewInDB, ReviewResponse, ReviewUpdate
from asyncpg import Record


class ReviewRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db

    @staticmethod
    def record_to_review(record: Record) -> ReviewInDB:
        """"""
        return ReviewInDB(
            booking_id=str(record["booking_id"]),
            client_id=str(record["client_id"]),
            technician_id=str(record["technician_id"]),
            rating=record["rating"],
            comment=record["comment"],
            review_id=str(record["review_id"]),
            created_at=record["created_at"]
        )

    async def get_all_reviews(self) -> List[ReviewInDB]:
        """"""
        records = await self.db.fetch("SELECT * FROM review")
        return [ReviewRepository.record_to_review(r) for r in records]

    async def get_review_by_id(self, review_id: str) -> Optional[ReviewInDB]:
        """"""
        record = await self.db.fetchrow(
            "SELECT * FROM review WHERE review_id = $1",
            uuid.UUID(review_id)
            )
        return ReviewRepository.record_to_review(record) if record is not None else None
    
    async def get_all_reviews_by_client_id(self, client_id: str) -> List[ReviewInDB]:
        """"""
        return await self._get_by("client_id", uuid.UUID(client_id))
    
    async def get_all_reviews_by_technician_id(self, technician_id: str) -> List[ReviewInDB]:
        """"""
        return await self._get_by("technician_id", uuid.UUID(technician_id))
    
    async def get_all_reviews_by_booking_id(self, booking_id: str) -> List[ReviewInDB]:
        """"""
        return await self._get_by("booking_id", uuid.UUID(booking_id))
    
    async def _get_by(self, column_name: str, value: Any) -> List[ReviewInDB]:
        """"""
        records = await self.db.fetch(
            f"SELECT * FROM review WHERE {column_name} = $1",
            value
            )
        return [ReviewRepository.record_to_review(r) for r in records]
    
    async def create_review(self, review_data: ReviewCreate) -> ReviewInDB:
        """"""
        id = await self.db.fetchrow(
            """
            INSERT INTO review (
                booking_id, client_id, technician_id,
                rating, comment
            )
            VALUES ($1, $2, $3, $4, $5)
            RETIRNING review_id
            """,
            review_data.booking_id,
            review_data.client_id,
            review_data.technician_id,
            review_data.rating,
            review_data.comment,
        )
        return await self.get_review_by_id(id)
    
    async def delete_review(self, review_id: str) -> bool:
        """"""
        result = await self.db.execute(
            "DELETE FROM review WHERE review_id = $1",
            uuid.UUID(review_id)
            )
        return result == "DELETE 0"
    
    async def update_review(self, review_id: str, update_data: ReviewUpdate) -> ReviewInDB:
        """"""
        fields: dict = {
            "rating": update_data.rating,
            "comment": update_data.comment
        }

        fields = {k: v for k, v in fields.items() if v is not None}

        if len(fields) == 0: return self.get_review_by_id(review_id)

        updates: list = [f"{k} = ${i}" for i, k in enumerate(fields.keys(), start=2)]
        values: list = [uuid.UUID(review_id), *tuple(fields.values())]

        query: str = f"""
        UPDATE review SET {', '.join(updates)}
        WHERE review_id = $1
        """

        await self.db.execute(query, *values)

        return await self.get_review_by_id(review_id)
