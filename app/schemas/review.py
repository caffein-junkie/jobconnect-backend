from typing import Optional
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from uuid import uuid4


class ReviewBase(BaseModel):
    booking_id: UUID4 = Field(..., description="Unique identifier for the booking")
    client_id: UUID4 = Field(..., description="Unique identifier for the client")
    technician_id: UUID4 = Field(..., description="Unique identifier for the technician")
    rating: float = Field(..., ge=0, le=5, description="Rating from 0 to 5 stars")
    comment: str = Field(..., min_length=1, max_length=1000, description="Review comment text")

    class Config:
        schema_extra = {
            "example": {
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "rating": 4.5,
                "comment": "Great service! The technician was punctual and professional."
            }
        }


class ReviewInDB(ReviewBase):
    review_id: UUID4 = Field(..., description="Unique identifier for the review")
    created_at: datetime = Field(..., description="Timestamp when review was created")

    class Config:
        schema_extra = {
            "example": {
                "review_id": "d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a44",
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "rating": 4.5,
                "comment": "Great service! The technician was punctual and professional.",
                "created_at": "2023-01-15T10:30:00Z"
            }
        }


class ReviewCreate(ReviewBase):
    class Config:
        schema_extra = {
            "example": {
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "rating": 4.5,
                "comment": "Great service! The technician was punctual and professional."
            }
        }


class ReviewResponse(ReviewBase):
    review_id: UUID4 = Field(..., description="Unique identifier for the review")
    created_at: datetime = Field(..., description="Timestamp when review was created")

    class Config:
        schema_extra = {
            "example": {
                "review_id": "d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a44",
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "rating": 4.5,
                "comment": "Great service! The technician was punctual and professional.",
                "created_at": "2023-01-15T10:30:00Z"
            }
        }


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0, le=5, description="Updated rating from 0 to 5 stars")
    comment: Optional[str] = Field(None, min_length=1, max_length=1000, description="Updated review comment text")

    class Config:
        schema_extra = {
            "example": {
                "rating": 5.0,
                "comment": "After further consideration, I'm upgrading my rating to 5 stars!"
            }
        }
        