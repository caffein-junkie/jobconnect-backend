from fastapi import APIRouter, Request, Depends
from typing import List
from app.database.database import AsyncDatabase
from app.schemas.technician import TechnicianResponse, TechnicianCreate, TechnicianUpdate
from app.repositories.technician import TechnicianRepository
from app.services.technician import TechnicianService

router: APIRouter = APIRouter()


async def get_db(request: Request) -> AsyncDatabase:
    """"""
    return request.app.state.db

async def get_technician_repository(db: AsyncDatabase = Depends(get_db)):
    """"""
    return TechnicianRepository(db)

async def get_technician_service(repo: TechnicianRepository = Depends(get_technician_repository)):
    """"""
    return TechnicianService(repo)


@router.get("/technician/{technician_id}", response_model=TechnicianResponse)
async def get_technician(
    technician_id: str,
    service: TechnicianService = Depends(get_technician_service)
    ):
    """"""
    return await service.get_technician(technician_id)


@router.get("/technician", response_model=List[TechnicianResponse])
async def get_all_technicians(
    service: TechnicianService = Depends(get_technician_service)
    ):
    """"""
    return await service.get_all_technicians()


@router.post("/technician", response_model=TechnicianResponse)
async def create_technician(
    technician_data: TechnicianCreate,
    service: TechnicianService = Depends(get_technician_service)
):
    """"""
    return await service.create_technician(technician_data)


@router.delete("/technician{technician_id}")
async def delete_technician(
    technician_id: str,
    service: TechnicianService = Depends(get_technician_service)
):
    """"""
    result = await service.delete_technician(technician_id)
    return {"result": result}


@router.put("/technician/{technician_id}", response_model=TechnicianResponse)
async def update_technician(
    technician_id: str,
    update_data: TechnicianUpdate,
    service: TechnicianService = Depends(get_technician_service)
):
    """"""
    return await service.update_technician(technician_id, update_data)
