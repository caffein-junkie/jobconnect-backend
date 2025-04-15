from typing import List, Optional
from app.schemas.notification import NotificationCreate, NotificationInDB, NotificationResponse
from app.repositories.notification import NotificationRepository


class NotificationService:

    def __init__(self, repo: NotificationRepository) -> None:
        self.repo = repo
    
    @staticmethod
    def notification_in_db_to_response(notification: NotificationInDB) -> NotificationResponse:
        """"""
        return NotificationResponse(
            notification_id=notification.notification_id,
            client_id=notification.client_id,
            technician_id=notification.technician_id,
            message=notification.message,
            is_read=notification.is_read,
            created_at=notification.created_at
        )
    
    async def create_notification(self, notification_data: NotificationCreate) -> NotificationResponse:
        """"""
        notification = await self.repo.create(notification_data)
        return NotificationService.notification_in_db_to_response(notification)
    
    async def delete_notification(self, notification_id: str) -> None:
        """"""
        await self.repo.delete(notification_id)

    async def update_notification_read_status(self, notification_id: str) -> bool:
        """"""
        return await self.repo.update_read_status(notification_id)
    
    async def get_all_client_notifications(self, client_id: str) -> List[NotificationResponse]:
        """"""
        notifications = await self.repo.get_all_notifications_by_user_id(client_id, "client")
        return [NotificationService.notification_in_db_to_response(n) for n in notifications]
    
    async def get_all_technician_notifications(self, technician_id: str) -> List[NotificationResponse]:
        """"""
        notifications = await self.repo.get_all_notifications_by_user_id(technician_id, "technician")
        return [NotificationService.notification_in_db_to_response(n) for n in notifications]
