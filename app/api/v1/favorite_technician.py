from fastapi import APIRouter, Request, Depends
from typing import List
from app.database.database import AsyncDatabase
from app.schemas.favorite_technician import FavoriteTechnicianCreate, FavoriteTechnicianResponse
from app.repositories.favorite_technician import FavoriteTechnicianRepository
from app.services.favorite_technician import FavoriteTechnicianService

router: APIRouter = APIRouter()

async def get_db(request: Request) -> AsyncDatabase:
    """"""
    return request.app.state.db

async def get_favorite_technician_repository(db: AsyncDatabase = Depends(get_db)):
    """"""
    return FavoriteTechnicianRepository(db)

async def get_favorite_technician_service(repo: FavoriteTechnicianRepository = Depends(get_favorite_technician_repository)):
    """"""
    return FavoriteTechnicianService(repo)


@router.post("/favorite_technician", response_model=FavoriteTechnicianResponse)
async def add_favorite_technician(
    ft_data: FavoriteTechnicianCreate,
    service: FavoriteTechnicianService = Depends(get_favorite_technician_service)
):
    """"""
    return await service.create_favorite_technician(ft_data)


@router.get("/favorite_technician/{client_id}", response_model=List[FavoriteTechnicianResponse])
async def get_favorite_technicians(
    client_id: str,
    service: FavoriteTechnicianService = Depends(get_favorite_technician_service)
):
    """"""
    return await service.get_favorite_technicians(client_id)

@router.delete("/favorite_technicians/{client_id}")
async def remove_favorite_technicians(
    client_id: str,
    technician_id: str,
    service: FavoriteTechnicianService = Depends(get_favorite_technician_service)
):
    """"""
    return await service.detete_favorite_technician(client_id)
