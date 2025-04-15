from typing import List
from app.schemas.technician import (
    TechnicianInDB,
    TechnicianResponse,
    TechnicianUpdate,
    TechnicianCreate
    )
from app.repositories.technician import TechnicianRepository
from app.utils.security import SecurityUtils
from app.utils.exceptions import (
    NotFoundException,
    InvalidCredentialsException
)


class TechnicianService:

    def __init__(self, repo: TechnicianRepository) -> None:
        self.repo = repo
    
    @staticmethod
    def technician_in_db_to_response(technician: TechnicianInDB) -> TechnicianResponse:
        """"""
        return TechnicianResponse(
            name=technician.name,
            surname=technician.surname,
            email=technician.email,
            phone_number=technician.phone_number,
            location_name=technician.location_name,
            longitude=technician.longitude,
            latitude=technician.latitude,
            service_types=technician.service_types,
            is_verified=technician.is_verified,
            technician_id=technician.technician_id,
            created_at=technician.created_at,
            experience_years=technician.experience_years,
            is_available=technician.is_available
        )
    
    async def get_all_technicians(self) -> List[TechnicianResponse]:
        """"""
        technicians = await self.repo.get_all()
        return [TechnicianService.technician_in_db_to_response(t) for t in technicians]
    
    async def get_technician_by_id(self, technician_id: str) -> TechnicianResponse:
        """"""
        technician = await self.repo.get_by_id(technician_id)
        if technician is None:
            raise NotFoundException("Technician not found")
        return TechnicianService.technician_in_db_to_response(technician)
    
    async def get_technician_by_email(self, email: str) -> TechnicianResponse:
        """"""
        technician = await self.repo.get_by_email(email)
        if technician is None:
            raise NotFoundException("Technician not found")
        return TechnicianService.technician_in_db_to_response(technician)
    
    async def create_technician(self, technician_data: TechnicianCreate) -> TechnicianResponse:
        """"""
        technician = await self.repo.create(technician_data)
        return TechnicianService.technician_in_db_to_response(technician)
    
    async def delete_technician(self, technician_id: str) -> bool:
        """"""
        return await self.repo.delete(technician_id)
    
    async def update_technician(
        self,
        technician_id: str,
        update_data: TechnicianUpdate
    ) -> TechnicianResponse:
        """"""
        updated_technician = await self.repo.update(technician_id, update_data)
        return TechnicianService.technician_in_db_to_response(updated_technician)

    async def authenticate_technician_with_email_and_password(self, email: str, password: str) -> TechnicianResponse:
        """"""
        raise NotImplementedError("authentication has not been implemented yet.")
        # technician = await self.repo.get_by_email(email)
        # if not technician:
        #     raise InvalidCredentialsException()
        # if not SecurityUtils.verify_password(password, technician.password_hash):
        #     raise InvalidCredentialsException()
        # if not technician.is_active:
        #     raise InvalidCredentialsException("Client account is inactive")
        # return TechnicianService.technician_in_db_to_response(technician)
