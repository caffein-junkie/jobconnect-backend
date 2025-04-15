from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BaseNotification(BaseModel):
    message: str = Field(..., description="Notification message")
    client_id: Optional[str] = Field(..., description="Unique identifier for the client")
    technician_id: Optional[str] = Field(..., description="Unique identifier for the technician")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Your booking has been confirmed",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": None,
            }
        }


class NotificationCreate(BaseNotification):
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Your booking has been confirmed",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": None,
            }
        }


class NotificationInDB(BaseNotification):
    notification_id: str = Field(..., description="The unique identifier for the notification")
    is_read: bool = Field(..., description="Whether the notification has been read or not")
    created_at: datetime = Field(..., description="Timestamp when notification was created")

    class Config:
        json_schema_extra = {
            "example": {
                "notification_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "message": "Your booking has been confirmed",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": None,
                "is_read": False,
                "created_at": "2023-01-15T10:30:00Z"
            }
        }

class NotificationResponse(BaseNotification):
    notification_id: str = Field(..., description="The unique identifier for the notification")
    is_read: bool = Field(..., description="Whether the notification has been read or not")
    created_at: datetime = Field(..., description="Timestamp when notification was created")

    class Config:
        json_schema_extra = {
            "example": {
                "notification_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "message": "Your booking has been confirmed",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": None,
                "is_read": False,
                "created_at": "2023-01-15T10:30:00Z"
            }
        }
