from typing import List
from app.schemas.admin import AdminCreate, AdminUpdate, AdminInDB, AdminResponse
from app.repositories.admin import AdminRepository
from app.utils.exceptions import (
    NotFoundException,
    InvalidCredentialsException,
)
from app.utils.security import SecurityUtils


class AdminService:

    def __init__(self, repo: AdminRepository) -> None:
        self.repo = repo
    
    @staticmethod
    def admin_in_db_to_response(admin: AdminInDB) -> AdminResponse:
        """"""
        response = AdminResponse(
            name=admin.name,
            surname=admin.surname,
            email=admin.email,
            phone_number=admin.phone_number,
            admin_id=admin.admin_id,
            role=admin.role,
            created_at=admin.created_at
        )
        return response
    
    async def create_admin(self, admin_data: AdminCreate) -> AdminResponse:
        """"""
        admin = await self.repo.create(admin_data)
        return AdminService.admin_in_db_to_response(admin)
    
    async def get_all_admins(self) -> List[AdminResponse]:
        """"""
        admins = await self.repo.get_all()
        return [AdminService.admin_in_db_to_response(a) for a in admins] 
    
    async def get_by_id(self, admin_id: str) -> AdminResponse:
        """"""
        admin = await self.repo.get_by_id(admin_id)
        if not admin: raise NotFoundException(f"Admin with id '{admin_id}' not found")
        return AdminService.admin_in_db_to_response(admin)
    
    async def get_by_email(self, email: str) -> AdminResponse:
        """"""
        admin = await self.repo.get_by_email(email)
        if not admin: raise NotFoundException(f"Admin with email '{email}' not found")
        return AdminService.admin_in_db_to_response(admin)
    
    async def authenticate_admin_with_email_and_password(self, email: str, password: str) -> AdminResponse:
        """"""
        admin = await self.repo.get_by_email(email)
        if not admin:
            raise InvalidCredentialsException()
        if not SecurityUtils.verify_password(password, admin.password_hash):
            raise InvalidCredentialsException()
        return AdminService.admin_in_db_to_response(admin)
    
    async def update_admin(
        self,
        admin_id: str,
        update_data: AdminUpdate,
        ) -> AdminResponse:
        """"""
        admin = await self.repo.update(admin_id, update_data)
        return AdminService.admin_in_db_to_response(admin)
    
    async def delete_admin(self, admin_id: str) -> None:
        """"""
        await self.repo.delete(admin_id)
