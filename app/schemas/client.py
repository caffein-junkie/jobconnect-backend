from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from pydantic_extra_types.coordinate import Latitude, Longitude
import re

class ClientBase(BaseModel):
    """Base schema with common fields"""
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=10)
    location_name: str
    latitude: Latitude
    longitude: Longitude
    is_active: Optional[bool] = True

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Phone number must be 10 digits')
        return v

class ClientCreate(ClientBase):
    """Schema for client registration"""
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Moses",
                "surname": "Kubeka",
                "email": "client@example.com",
                "phone_number": "0798765435",
                "password": "securepassword123",
                "location_name": "Soshanguve",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "is_active": True
            }
        }

class ClientInDB(ClientBase):
    """Database representation (includes sensitive fields)"""
    client_id: str
    password_hash: str
    last_login: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ClientResponse(ClientBase):
    """What's returned to the client (excludes sensitive data)"""
    client_id: str
    last_login: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ClientUpdate(BaseModel):
    """Schema for partial updates"""
    name: Optional[str] = Field(None, max_length=50)
    surname: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=10)
    password: Optional[str] = Field(None, min_length=8)
    location_name: Optional[str] = None
    latitude: Optional[Latitude] = None
    longitude: Optional[Longitude] = None
    is_active: Optional[bool] = None

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None and not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Phone number must be 10 digits')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Moses",
                "surname": "Kubeka",
                "email": "client@example.com",
                "phone_number": "0798765435",
                "password": "securepassword123",
                "location_name": "Soshanguve",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }

class ClientLogin(BaseModel):
    """Schema for login requests"""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "client@example.com",
                "password": "securepassword123"
            }
        }
