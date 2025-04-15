import uuid
from typing import List, Literal
from asyncpg import Record
from app.database.database import AsyncDatabase
from app.schemas.notification import NotificationInDB, NotificationCreate


class NotificationRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db
    
    @staticmethod
    def record_to_notification(record: Record) -> NotificationInDB:
        """"""
        return NotificationInDB(
            notification_id=str(record["notification_id"]),
            client_id=str(record["client_id"]) if record["client_id"] is not None else None,
            technician_id=str(record["technician_id"]) if record["technician_id"] is not None else None,
            message=record["message"],
            is_read=record["is_read"],
            created_at=record["created_at"]
        )
    
    async def create(self, notification_data: NotificationCreate) -> NotificationInDB:
        """"""
        query: str = """
        INSERT INTO notification (client_id, technician_id, message)
        VALUES ($1, $2, $3)
        RETURNING notification_id, client_id, technician_id, message, is_read, created_at
        """
        record: Record = await self.db.fetchrow(
            query,
            notification_data.client_id,
            notification_data.technician_id,
            notification_data.message
            )
        return NotificationRepository.record_to_notification(record) if record else None
    
    async def get_all_notifications_by_user_id(
        self,
        user_id: str,
        name: Literal["client", "technician"]
        ) -> List[NotificationInDB]:
        """"""
        records = await self.db.fetch(f"SELECT * FROM notification WHERE {name.lower()} = $1", uuid.UUID(user_id))
        return [NotificationRepository.record_to_notification(r) for r in records]
    
    async def update_read_status(self, notification_id: str) -> bool:
        """"""
        query: str = """
        UPDATE notifiation SET is_read = TRUE
        WHERE notification_id = $1
        RETURNING notification_id
        """
        nid = await self.db.fetchrow(query, uuid.UUID(notification_id))
        return True if nid else False
    
    async def delete(self, notification_id: str) -> None:
        """"""
        query: str = """
        DELETE FROM notification WHERE notification_id = $1
        """
        await self.db.execute(query, uuid.UUID(notification_id))
