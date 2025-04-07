import uuid
from typing import Optional, List
from asyncpg import Record
from datetime import datetime, timezone
from app.database.database import AsyncDatabase
from app.schemas.client import ClientCreate, ClientInDB, ClientUpdate
from app.utils.security import SecurityUtils
from app.utils.exceptions import DuplicateEntryException, NotFoundException

class ClientRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db
    
    def _record_to_client(self, record: Record) -> ClientInDB:
        """"""
        return ClientInDB(
            name=record["name"],
            surname=record["surname"],
            email=record["email"],
            phone_number=record["phone_number"],
            location_name=record["location_name"],
            latitude=record["longitude"],
            longitude=record["longitude"],
            is_active=record["is_active"],
            client_id=str(record["client_id"]),
            password_hash=record["password_hash"],
            last_login=record["last_login"],
            created_at=record["created_at"]
        )

    async def get_all(self) -> List[ClientInDB]:
        """"""
        records = await self.db.fetch(
            """
            SELECT 
                client_id,
                name,
                surname,
                email,
                phone_number,
                password_hash,
                location_name,
                ST_X(location::geometry) AS longitude,
                ST_Y(location::geometry) AS latitude,
                is_active,
                last_login,
                created_at
            FROM clients 
            """
        )
        return [self._record_to_client(r) for r in records]

    async def get_by_id(self, client_id: str) -> Optional[ClientInDB]:
        """"""
        record = await self.db.fetchrow(
            """
            SELECT 
                client_id,
                name,
                surname,
                email,
                phone_number,
                password_hash,
                location_name,
                ST_X(location::geometry) AS longitude,
                ST_Y(location::geometry) AS latitude,
                is_active,
                last_login,
                created_at
            FROM clients 
            WHERE client_id = $1
            """,
            uuid.UUID(client_id)
            )
        return self._record_to_client(record) if record else None
    
    async def get_by_email(self, email: str) -> Optional[ClientInDB]:
        """"""
        record = await self.db.fetchrow(
            """
            SELECT 
                client_id,
                name,
                surname,
                email,
                phone_number,
                password_hash,
                location_name,
                ST_X(location::geometry) AS longitude,
                ST_Y(location::geometry) AS latitude,
                is_active,
                last_login,
                created_at
            FROM clients 
            WHERE email = $1
            """,
            email
            )
        return self._record_to_client(record) if record is not None else None
    
    async def create(self, client_data: ClientCreate) -> ClientInDB:
        """"""
        if await self.get_by_email(client_data.email):
            raise DuplicateEntryException()
        
        hashed_password: str = SecurityUtils.hash_password(client_data.password)
        point: str = f"POINT({client_data.longitude} {client_data.latitude})"
        query: str = """
        INSERT INTO clients (
            name, surname, email, phone_number,
            password_hash, location_name, location, is_active
        )
        VALUES ($1, $2, $3, $4, $5, $6, ST_GeomFromText($7), $8)
        """
        await self.db.execute(
            query,
            client_data.name,
            client_data.surname,
            client_data.email,
            client_data.phone_number,
            hashed_password,
            client_data.location_name,
            point,
            client_data.is_active
        )
        return await self.get_by_email(client_data.email)
    
    async def update(
        self,
        client_id: str,
        update_data: ClientUpdate, 
    ) -> ClientInDB:
        """"""
        updates: list = []
        params: list = []
        param_count: int = 1

        fields = {
            "name": update_data.name,
            "surname": update_data.surname,
            "email": update_data.email,
            "phone_number": update_data.phone_number,
            "location_name": update_data.location_name,
            "is_active": update_data.is_active
        }

        if update_data.password is not None:
            fields["password_hash"] = SecurityUtils.hash_password(update_data.password)
        
        if update_data.latitude is not None or update_data.longitude is not None:
            if None in (update_data.latitude, update_data.longitude):
                current = await self.get_by_id(client_id)
                if not current:
                    raise NotFoundException("Client not found")
                lat = update_data.latitude if update_data.latitude is not None else current.latitude
                lon = update_data.longitude if update_data.longitude is not None else current.longitude
            else:
                lat = update_data.latitude
                lon = update_data.longitude
        
        updates.append(f"location = ST_GeogFromText('POINT({lon} {lat})')")

        for field, value in fields.items():
            if value is not None:
                updates.append(f"{field} = ${param_count}")
                params.append(value)
                param_count += 1
        
        if not updates:
            return await self.get_by_id(client_id)
        
        query: str = f"""
        UPDATE clients SET {', '.join(updates)}
        WHERE client_id = ${param_count}
        """
        params.append(uuid.UUID(client_id))

        await self.db.execute(query, *params)
        return await self.get_by_id(client_id)
    
    async def update_last_login(self, client_id: str) -> None:
        await self.db.execute(
            "UPDATE clients SET last_login = $1 WHERE client_id = $2",
            datetime.now(timezone.utc()),
            uuid.UUID(client_id)
        )

    async def deactivate(self, client_id: str) -> None:
        """"""
        await self.db.execute(
            "UPDATE clients SET is_active = FALSE WHERE client_id = $1",
            uuid.UUID(client_id)
        )

    async def delete(self, client_id: str) -> None:
        """"""
        result = await self.db.execute(
            "DELETE FROM clients WHERE client_id = $1",
            uuid.UUID(client_id)
        )
        if result == "DELETE 0":
            raise NotFoundException("Client not found")
        
    async def add_favorite_technicians(self, client_id: str, technician_id: str) -> bool:
        """"""
        favorite = await self.db.fetchrow(
            """
            SELECT * FROM favorite_technicians
            WHERE client_id = $1 AND technician_id = $2
            """
            )
