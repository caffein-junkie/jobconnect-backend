from enum import Enum
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class BookingStatus(str, Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class BookingBase(BaseModel):
    client_id: str
    technician_id: str
    service_type: str
    description: str
    price: float
    status: BookingStatus
    start_date: datetime
    end_date: datetime


class BookingCreate(BookingBase):

    model_config = ConfigDict(from_attributes=True)


class BookingInDB(BookingBase):
    booking_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingUpdate(BaseModel):
    description: str
    price: float
    status: BookingStatus
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BookingResponse(BookingBase):

    model_config = ConfigDict(from_attributes=True)
