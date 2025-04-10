from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from pydantic_extra_types.coordinate import Latitude, Longitude
import re

class TechnicianBase(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=10)
    location_name: str
    latitude: Latitude
    longitude: Longitude
    service_types: List[str] = Field(..., min_length=1)
    is_verified: bool = False
    is_available: bool = True
    experience_years: int = Field(..., ge=0)

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Phone number must be 10 digits')
        return v

    @field_validator('service_types')
    def validate_service_types(cls, v):
        if not v:
            raise ValueError('At least one service type is required')
        return v

class TechnicianCreate(TechnicianBase):
    """Schema for technician registration"""
    password: str = Field(..., min_length=8)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John",
                "surname": "Matlala",
                "email": "tech@example.com",
                "phone_number": "0667651235",
                "password": "securepassword123",
                "location_name": "Soshanguve",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "service_types": ["plumbing", "electrical"],
                "is_available": True
            }
        }
    )

class TechnicianInDB(TechnicianBase):
    """Database representation (includes sensitive fields)"""
    technician_id: str
    password_hash: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TechnicianResponse(TechnicianBase):
    """What's returned to the client (excludes sensitive data)"""
    technician_id: str
    last_login: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TechnicianUpdate(BaseModel):
    """Schema for partial updates"""
    name: Optional[str] = Field(None, max_length=50)
    surname: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=10)
    password: Optional[str] = Field(None, min_length=8)
    location_name: Optional[str] = None
    latitude: Optional[Latitude] = None
    longitude: Optional[Longitude] = None
    service_types: Optional[List[str]] = None
    is_verified: Optional[bool] = None
    is_available: Optional[bool] = None
    experience_years: Optional[int] = None

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None and not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Phone number must be 10 digits')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Name",
                "service_types": ["plumbing", "hvac"],
                "latitude": 34.0522
            }
        }
    )

class TechnicianLogin(BaseModel):
    """Schema for login requests"""
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "tech@example.com",
                "password": "securepassword123"
            }
        }
    )