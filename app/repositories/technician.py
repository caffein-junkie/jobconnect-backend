import uuid
from typing import Optional, List
from asyncpg import Record
from datetime import datetime, timezone
from app.database.database import AsyncDatabase
from app.schemas.technician import TechnicianCreate, TechnicianInDB, TechnicianUpdate
from app.utils.security import SecurityUtils
from app.utils.exceptions import DuplicateEntryException, NotFoundException


class TechnicianRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db
    
    @staticmethod
    def record_to_technician(record: Record) -> TechnicianInDB:
        """"""
        return TechnicianInDB(
            name=record["name"],
            surname=record["surname"],
            email=record["email"],
            phone_number=record["phone_number"],
            location_name=record["location_name"],
            latitude=record["longitude"],
            longitude=record["longitude"],
            service_types=record["service_types"],
            is_verified=record["is_verified"],
            technician_id=str(record["technician_id"]),
            password_hash=record["password_hash"],
            created_at=record["created_at"],
            is_available=record["is_available"],
            experience_years=record["experience_years"]
        )
    
    async def get_all(self) -> List[TechnicianInDB]:
        """"""
        records = await self.db.fetch(
            """
            SELECT 
                technician_id,
                name,
                surname,
                email,
                phone_number,
                password_hash,
                location_name,
                ST_X(location::geometry) AS longitude,
                ST_Y(location::geometry) AS latitude,
                service_types,
                is_verified,
                experience_years,
                is_available,
                created_at
            FROM technician 
            """
        )
        return [TechnicianRepository.record_to_technician(r) for r in records]

    async def get_by_id(self, technician_id: str) -> Optional[TechnicianInDB]:
        """"""
        record = await self.db.fetchrow(
            """
            SELECT 
                technician_id,
                name,
                surname,
                email,
                phone_number,
                password_hash,
                location_name,
                ST_X(location::geometry) AS longitude,
                ST_Y(location::geometry) AS latitude,
                service_types,
                is_verified,
                experience_years,
                is_available,
                created_at
            FROM technician 
            WHERE technician_id = $1
            """,
            uuid.UUID(technician_id)
        )
        return TechnicianRepository.record_to_technician(record) if record is not None else None
    
    async def get_by_email(self, email: str) -> Optional[TechnicianInDB]:
        """"""
        record = await self.db.fetchrow(
            """
            SELECT 
                technician_id,
                name,
                surname,
                email,
                phone_number,
                password_hash,
                location_name,
                ST_X(location::geometry) AS longitude,
                ST_Y(location::geometry) AS latitude,
                service_types,
                is_verified,
                experience_years,
                is_available,
                created_at
            FROM technician 
            WHERE email = $1
            """,
            email
        )
        return TechnicianRepository.record_to_technician(record) if record is not None else None

    async def create(self, technician_data: TechnicianCreate) -> TechnicianInDB:
        """"""
        if await self.get_by_email(technician_data.email):
            raise DuplicateEntryException()
        
        hashed_password: str = SecurityUtils.hash_password(technician_data.password)
        point: str = f"POINT({technician_data.longitude} {technician_data.latitude})"
        query: str = """
        INSERT INTO technician (
            name, surname, email, phone_number,
            password_hash, location_name, location,
            service_types, is_verified, experience_years, is_available
        )
        VALUES ($1, $2, $3, $4, $5, $6, ST_GeomFromText($7), $8, $9, $10, $11)
        """
        await self.db.execute(
            query,
            technician_data.name,
            technician_data.surname,
            technician_data.email,
            technician_data.phone_number,
            hashed_password,
            technician_data.location_name,
            point,
            technician_data.service_types,
            technician_data.is_verified,
            technician_data.experience_years,
            technician_data.is_available
        )
        return await self.get_by_email(technician_data.email)
    
    async def delete(self, technician_id: str) -> bool:
        """"""
        await self.db.execute(
            "DELETE FROM technician WHERE technician_id = $1",
            uuid.UUID(technician_id)
            )
    
    async def update(self, technician_id: str, update_data: TechnicianUpdate) -> TechnicianInDB:
        """"""
        updates = []
        params = []
        param_count = 1

        fields = {
            "name": update_data.name,
            "surname": update_data.surname,
            "email": update_data.email,
            "phone_number": update_data.phone_number,
            "location_name": update_data.location_name,
            "service_types": update_data.service_types,
            "is_verified": update_data.is_verified,
        }

        # Handle password update
        if update_data.password:
            fields["password_hash"] = SecurityUtils.hash_password(update_data.password)

        # Handle location update
        if update_data.latitude is not None or update_data.longitude is not None:
            if None in (update_data.latitude, update_data.longitude):
                current = await self.get_by_id(technician_id)
                if not current:
                    raise NotFoundException("Technician not found")
                lat = update_data.latitude if update_data.latitude is not None else current.latitude
                lon = update_data.longitude if update_data.longitude is not None else current.longitude
            else:
                lat = update_data.latitude
                lon = update_data.longitude
            
            updates.append(f"location = ST_GeogFromText('POINT({lon} {lat})')")

        # Add regular fields to updates
        for field, value in fields.items():
            if value is not None:
                updates.append(f"{field} = ${param_count}")
                params.append(value)
                param_count += 1

        if not updates:
            return await self.get_by_id(technician_id)

        query: str = f"""
        UPDATE technician SET {', '.join(updates)}
        WHERE technician_id = ${param_count}
        """
        params.append(uuid.UUID(technician_id))

        await self.db.execute(query, *params)
        return await self.get_by_id(technician_id)
    