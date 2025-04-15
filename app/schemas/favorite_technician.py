from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FavoriteTechnicianBase(BaseModel):
    client_id: str
    technician_id: str

    model_config = ConfigDict(from_attributes=True)


class FavoriteTechnicianCreate(FavoriteTechnicianBase):

    class Config:
        json_schema_extra = {
            "example": {
                "client_id": "f7faf529-a8fa-4dcf-8d6a-5eb444fa639c",
                "technician_id": "595a4e92-2a7c-4ad6-877e-5eeb05aa4b55",
            }
        }


class FavoriteTechnicianInDB(FavoriteTechnicianBase):
    favorite_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FavoriteTechnicianResponse(FavoriteTechnicianBase):
    favorite_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
