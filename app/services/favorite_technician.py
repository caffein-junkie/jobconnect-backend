from typing import Optional, List
from app.schemas.favorite_technician import (
    FavoriteTechnicianInDB,
    FavoriteTechnicianResponse,
    FavoriteTechnicianCreate
)
from app.repositories.favorite_technician import FavoriteTechnicianRepository
from app.utils.exceptions import DuplicateEntryException


class FavoriteTechnicianService:

    def __init__(self, repo: FavoriteTechnicianRepository) -> None:
        self.repo = repo
    
    @staticmethod
    def ft_in_db_to_response(ft: FavoriteTechnicianInDB) -> FavoriteTechnicianResponse:
        return FavoriteTechnicianResponse(
            client_id=ft.client_id,
            technician_id=ft.technician_id,
            favorite_id=ft.favorite_id,
            created_at=ft.created_at
        )
    
    async def create_favorite_technician(self, ft_data: FavoriteTechnicianCreate) -> FavoriteTechnicianResponse:
        """"""
        ft = await self.repo.create(ft_data)
        return FavoriteTechnicianService.ft_in_db_to_response(ft)
    
    async def detete_favorite_technician(self, client_id: str, technician_id: str) -> None:
        """"""
        await self.repo.delete(client_id, technician_id)
    
    async def get_favorite_technicians(self, client_id: str) -> List[FavoriteTechnicianResponse]:
        """"""
        f_technicians = await self.repo.get_favorite_technicians_by_client_id(client_id)
        return [FavoriteTechnicianService.ft_in_db_to_response(t) for t in f_technicians]
