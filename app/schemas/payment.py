from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# Enums for better validation
class PaymentMethod(str, Enum):
    CARD = "card"
    BANKING = "banking"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentBase(BaseModel):
    booking_id: str = Field(..., description="The booking ID associated with this payment")
    client_id: str = Field(..., description="The client ID making the payment")
    technician_id: str = Field(..., description="The technician ID receiving the payment")
    amount: float = Field(..., gt=0, description="Payment amount (must be positive)")
    payment_method: PaymentMethod = Field(..., description="Payment method used")
    payment_status: PaymentStatus = Field(
        default=PaymentStatus.PENDING,
        description="Current status of the payment"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "amount": 99.99,
                "payment_method": "card",
                "payment_status": "pending"
            }
        }


class PaymentCreate(PaymentBase):
    class Config:
        json_schema_extra = {
            "example": {
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "amount": 99.99,
                "payment_method": "card"
                # payment_status omitted as it defaults to 'pending'
            }
        }


class PaymentInDB(PaymentBase):
    payment_id: str = Field(..., description="Unique identifier for the payment")
    transaction_date: Optional[datetime] = Field(..., description="Timestamp when payment was processed")

    class Config:
        json_schema_extra = {
            "example": {
                "payment_id": "d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a44",
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "amount": 99.99,
                "payment_method": "card",
                "payment_status": "completed",
                "transaction_date": "2023-01-15T10:30:00Z"
            }
        }


class PaymentResponse(PaymentBase):
    payment_id: str = Field(..., description="Unique identifier for the payment")
    transaction_date: Optional[datetime] = Field(..., description="Timestamp when payment was processed")

    class Config:
        json_schema_extra = {
            "example": {
                "payment_id": "d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a44",
                "booking_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "client_id": "b1ffc99-9c0b-4ef8-bb6d-6bb9bd380a22",
                "technician_id": "c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a33",
                "amount": 99.99,
                "payment_method": "card",
                "payment_status": "completed",
                "transaction_date": "2023-01-15T10:30:00Z"
            }
        }


class PaymentUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0, description="Updated payment amount")
    payment_method: Optional[PaymentMethod] = Field(None, description="Updated payment method")
    payment_status: Optional[PaymentStatus] = Field(None, description="Updated payment status")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 89.99,  # after discount
                "payment_status": "completed"  # marking as paid
            }
        }
