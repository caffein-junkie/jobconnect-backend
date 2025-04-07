import uuid
from datetime import datetime, timezone
from typing import Optional, List
from asyncpg import Record

from app.database.database import AsyncDatabase
from app.schemas.admin import AdminCreate, AdminInDB, AdminRole, AdminUpdate
from app.utils.security import SecurityUtils
from app.utils.exceptions import (
    NotFoundException,
    InvalidCredentialsException,
    DuplicateEntryException,
)


class AdminRepository:

    def __init__(self, db: AsyncDatabase) -> None:
        self.db = db
    
    @staticmethod
    def record_to_admin(record: Record) -> AdminInDB:
        """"""
        record = dict(record)
        return AdminInDB(
            name=record["name"],
            surname=record["surname"],
            email=record["email"],
            phone_number=record["phone_number"],
            admin_id=str(record["admin_id"]),
            password_hash=record["password_hash"],
            role=record["role"],
            is_active=record["is_active"],
            last_login=record["last_login"],
            created_at=record["created_at"]
        )
    
    async def get_all(self) -> List[AdminInDB]:
        """"""
        records = await self.db.fetch("SELECT * FROM admins")
        return [AdminRepository.record_to_admin(r) for r in records]
    
    async def get_by_id(self, admin_id: str) -> Optional[AdminInDB]:
        """"""
        record = await self.db.fetchrow(
            "SELECT * FROM admins WHERE admin_id = $1",
            uuid.UUID(admin_id)
        )
        return AdminRepository.record_to_admin(record) if record else None
    
    async def get_by_email(self, email: str) -> Optional[AdminInDB]:
        """"""
        record = await self.db.fetchrow(
            "SELECT * FROM admins WHERE email = $1", 
            email
        )
        return AdminRepository.record_to_admin(record) if record is not None else None
    
    async def create(self, admin_data: AdminCreate) -> AdminInDB:
        """"""
        if await self.get_by_email(admin_data.email):
            raise DuplicateEntryException()
        
        hashed_password: str = SecurityUtils.hash_password(admin_data.password)
        query: str = """
        INSERT INTO admins (
            name, surname, email, phone_number,
            password_hash, role, is_active
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        """
        await self.db.execute(
            query,
            admin_data.name,
            admin_data.surname,
            admin_data.email,
            admin_data.phone_number,
            hashed_password,
            admin_data.role or AdminRole.SUPPORT_ADMIN.value,
            admin_data.is_active if admin_data.is_active is not None else True
        )
        new_admin = await self.get_by_email(admin_data.email)
        with open("debug.txt", "w") as f: f.write(f"New admin: {new_admin}")
        return new_admin

    async def update(self, admin_id: str, update_data: AdminUpdate, current_admin: AdminInDB) -> AdminInDB:
        """"""
        if (update_data.role and
            update_data.role != current_admin.role and
            current_admin.role != AdminRole.SUPER_ADMIN
            ):
            raise PermissionError("Only super admins can modify admin roles")
        
        updates: list = []
        params: list = []
        param_count: int = 1

        fields = {
            "name": update_data.name,
            "surname": update_data.surname,
            "email": update_data.email,
            "phone_number": update_data.phone_number,
            "role": update_data.role,
            "is_active": update_data.is_active
        }

        if update_data.password is not None:
            fields["password_hash"] = SecurityUtils.hash_password(update_data.password)
        
        for field, value in fields.items():
            if value is not None:
                updates.append(f"{field} = ${param_count}")
                params.append(value)
                param_count += 1
        
        if not updates:
            return await self.get_by_id(admin_id)
        
        query: str = f"""
        UPDATE admins SET {', '.join(updates)}
        WHERE admin_id = ${param_count}
        """
        params.append(uuid.UUID(admin_id))

        await self.db.execute(query, *params)
        return await self.get_by_id(admin_id)

    async def update_last_login(self, admin_id: str) -> None:
        await self.db.execute(
            "UPDATE admins SET last_login = $1 WHERE admin_id = $2",
            datetime.now(timezone.utc()),
            uuid.UUID(admin_id)
        )

    async def deactivate(self, admin_id: str) -> None:
        """"""
        await self.db.execute(
            "UPDATE admins SET is_active = FALSE WHERE admin_id = $1",
            uuid.UUID(admin_id)
        )

    async def delete(self, admin_id: str) -> None:
        """"""
        result = await self.db.execute(
            "DELETE FROM admins WHERE admin_id = $1",
            uuid.UUID(admin_id)
        )
        if result == "DELETE 0":
            raise NotFoundException("Admin not found")
