from typing import List, Any
from fastapi import APIRouter, Request, Depends
from app.schemas.booking import BookingResponse, BookingCreate, BookingUpdate
from app.repositories.booking import BookingRepository
from app.services.booking import BookingService
from app.database.database import AsyncDatabase

router: APIRouter = APIRouter()

async def get_db(request: Request) -> AsyncDatabase:
    return request.app.db

async def get_booking_repository(db: AsyncDatabase = Depends(get_db)) -> BookingRepository:
    return BookingRepository(db)

async def get_booking_service(repo: BookingRepository = Depends(get_booking_repository)) -> BookingService:
    return BookingService(repo)


@router.post("/booking", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    service: BookingService = Depends(get_booking_service)
):
    """"""
    return await service.create_booking(booking_data)


@router.put("/booking/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: str,
    update_data: BookingUpdate,
    service: BookingService = Depends(get_booking_service)
):
    """"""
    return await service.update_booking(booking_id, update_data)


@router.delete("/booking/{booking_id}")
async def delete_booking(
    booking_id: str,
    service: BookingService = Depends(get_booking_service)
):
    """"""
    result = service.delete_booking(booking_id)
    return {"result": result}


@router.get("/booking", response_model=List[BookingResponse])
async def get_all_bookings(service: BookingService = Depends(get_booking_service)):
    """"""
    return await service.get_all_bookings()

@router.get("/booking/{booking_id}", response_model=BookingResponse)
async def get_booking_by(
    booking_id: str,
    service: BookingService = Depends(get_booking_service)
):
    """"""
    return await service.get_booking_by_id(booking_id)


@router.get("/booking/{column_name}", response_model=List[BookingResponse])
async def get_all_bookings_by(
    column_name: str,
    value: Any,
    service: BookingService = Depends(get_booking_service)
):
    """"""
    return await service.get_all_bookings_by(column_name, value)
