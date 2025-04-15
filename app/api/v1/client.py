from fastapi import APIRouter, Request, Depends
from typing import List
from app.database.database import AsyncDatabase
from app.schemas.client import ClientResponse, ClientCreate, ClientUpdate
from app.repositories.client import ClientRepository
from app.services.client import ClientService
from app.schemas.favorite_technician import FavoriteTechnicianCreate, FavoriteTechnicianResponse
from app.services.favorite_technician import FavoriteTechnicianService

router: APIRouter = APIRouter()


async def get_db(request: Request) -> AsyncDatabase:
    """"""
    return request.app.state.db

async def get_client_repository(db: AsyncDatabase = Depends(get_db)):
    """"""
    return ClientRepository(db)

async def get_client_service(repo: ClientRepository = Depends(get_client_repository)):
    """"""
    return ClientService(repo)


@router.get("/client/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: str,
    service: ClientService = Depends(get_client_service)
    ):
    """"""
    return await service.get_client(client_id)


@router.get("/client", response_model=List[ClientResponse])
async def get_all_clients(
    service: ClientService = Depends(get_client_service)
    ):
    """"""
    return await service.get_all_clients()


@router.post("/client", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    service: ClientService = Depends(get_client_service)
):
    """"""
    return await service.create_client(client_data)


@router.delete("/client{client_id}")
async def delete_client(
    client_id: str,
    service: ClientService = Depends(get_client_service)
):
    """"""
    await service.delete_client(client_id)
    return {"result": True}


@router.put("/client/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: str,
    update_data: ClientUpdate,
    service: ClientService = Depends(get_client_service)
):
    """"""
    return await service.update_client(client_id, update_data)
