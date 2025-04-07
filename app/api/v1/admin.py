from fastapi import APIRouter, Request, Depends
from typing import List
from app.database.database import AsyncDatabase
from app.schemas.admin import AdminResponse, AdminCreate, AdminUpdate, AdminInDB
from app.repositories.admin import AdminRepository
from app.services.admin import AdminService

router: APIRouter = APIRouter()


async def get_db(request: Request) -> AsyncDatabase:
    """"""
    return request.app.state.db


async def get_admin_repository(db: AsyncDatabase = Depends(get_db)):
    """"""
    return AdminRepository(db)

async def get_admin_service(repo: AdminRepository = Depends(get_admin_repository)):
    """"""
    return AdminService(repo)


@router.post("/admin", response_model=AdminResponse)
async def create(
    admin_data: AdminCreate,
    service: AdminService = Depends(get_admin_service)
    ):
    """"""
    return await service.create_admin(admin_data)


@router.get("/admin/{admin_id}", response_model=AdminResponse)
async def get_admin(
    admin_id: str,
    service: AdminService = Depends(get_admin_service)
    ):
    """"""
    return await service.get_by_id(admin_id)


@router.delete("/admin/{admin_id}")
async def delete_admin(
    admin_id: str,
    service: AdminService = Depends(get_admin_service)
    ):
    """"""
    await service.delete_admin(admin_id)
    return {"result": True}


@router.put("/admin/{admin_id}", response_model=AdminResponse)
async def update_admin(
    admin_id: str,
    update_data: AdminUpdate,
    current_admin: AdminInDB,
    service: AdminService = Depends(get_admin_service)
):
    """"""
    return await service.update_admin(admin_id, update_data, current_admin)


@router.get("/admin", response_model=List[AdminResponse])
async def get_all_admins(
    service: AdminService = Depends(get_admin_service)
):
    """"""
    return await service.get_all_admins()
