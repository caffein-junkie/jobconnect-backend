from fastapi import APIRouter, Request, Depends
from typing import List
from app.database.database import AsyncDatabase
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.repositories.notification import NotificationRepository
from app.services.notification import NotificationService

router: APIRouter = APIRouter()

def get_db(request: Request) -> AsyncDatabase:
    """"""
    return request.app.state.db

def get_notification_repository(db: AsyncDatabase = Depends(get_db)):
    """"""
    return NotificationRepository(db)

def get_notification_service(repo: NotificationRepository = Depends(get_notification_repository)):
    """"""
    return NotificationService(repo)


@router.post("/notification", response_model=NotificationResponse)
async def create_notification(
    notification_data: NotificationCreate,
    service: NotificationService = Depends(get_notification_service)
):
    """"""
    return await service.create_notification(notification_data)


@router.delete("/notification/{notification_id}")
async def delete_notification(
    notification_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """"""
    await service.delete_notification(notification_id)


@router.get("/notification/client", response_model=List[NotificationResponse])
async def delete_notification(
    client_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """"""
    await service.get_all_client_notifications(client_id)


@router.get("/notification/technician", response_model=List[NotificationResponse])
async def delete_notification(
    technician_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """"""
    await service.get_all_technician_notifications(technician_id)


@router.put("/notification/{notification_id}")
async def update_notification_read_status(
    notification_id: str,
    service: NotificationService = Depends(get_notification_service)
):
    """"""
    return {"result": await service.update_notification_read_status(notification_id)}
