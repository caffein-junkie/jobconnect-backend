from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class AdminRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    SUPPORT_ADMIN = "support_admin"
    CONTENT_ADMIN = "content_admin"


class AdminBase(BaseModel):
    name: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=10, pattern=r"^[0-9]{10}$")

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None and not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Phone number must be 10 digits')
        return v


class AdminCreate(AdminBase):
    password: str = Field(..., min_length=8)
    role: AdminRole
    is_active: Optional[bool] = True

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Bob",
                "surname": "Marley",
                "email": "marley@jobconnect.com",
                "phone_number": "0827398875",
                "password": "strongpassword123",
                "role": "support_admin",
                "is_active": True
            }
        }


class AdminInDB(AdminBase):
    admin_id: str
    password_hash: str
    role: AdminRole
    is_active: bool
    last_login: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class AdminResponse(AdminBase):
    admin_id: str
    role: AdminRole
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AdminUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    surname: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=10, pattern=r"^[0-9]{10}$")
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[AdminRole] = None
    is_active: Optional[bool] = None

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None and not re.match(r'^[0-9]{10}$', v):
            raise ValueError('Phone number must be 10 digits')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Bob",
                "surname": "Marley",
                "email": "marley@jobconnect.com",
                "phone_number": "0827398875",
                "password": "strongpassword123",
                "role": "support_admin",
                "is_active": True
            }
        }


class AdminLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "yourpassword123"
            }
        }


class AdminPasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

