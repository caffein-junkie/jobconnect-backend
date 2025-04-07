from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ReviewBase(BaseModel):
    booking_id: str
    client_id: str
    technician_id: str
    rating: float = Field(..., ge=0, le=5)
    comment: str


class ReviewInDB(ReviewBase):
    review_id: str
    created_at: datetime


class ReviewCreate(ReviewBase): ...


class ReviewResponse(ReviewBase):
    review_id: str
    created_at: datetime


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0, le=5)
    comment: Optional[str] = Field(None)
