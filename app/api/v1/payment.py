from typing import List, Any
from fastapi import APIRouter, Request, Depends
from app.schemas.payment import PaymentResponse, PaymentCreate, PaymentUpdate
from app.repositories.payment import PaymentRepository
from app.services.payment import PaymentService
from app.database.database import AsyncDatabase

router: APIRouter = APIRouter()

async def get_db(request: Request) -> AsyncDatabase:
    return request.app.state.db

async def get_payment_repository(db: AsyncDatabase = Depends(get_db)) -> PaymentRepository:
    return PaymentRepository(db)

async def get_payment_service(repo: PaymentRepository = Depends(get_payment_repository)) -> PaymentService:
    return PaymentService(repo)


@router.post("/payment", response_model=PaymentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    service: PaymentService = Depends(get_payment_service)
):
    """"""
    return await service.create_payment(payment_data)


@router.put("/payment/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: str,
    update_data: PaymentUpdate,
    service: PaymentService = Depends(get_payment_service)
):
    """"""
    return await service.update_payment(payment_id, update_data)


@router.delete("/payment/{payment_id}")
async def delete_payment(
    payment_id: str,
    service: PaymentService = Depends(get_payment_service)
):
    """"""
    result = service.delete_payment(payment_id)
    return {"result": result}


@router.get("/payment", response_model=List[PaymentResponse])
async def get_all_payments(service: PaymentService = Depends(get_payment_service)):
    """"""
    return await service.get_all_payments()

@router.get("/payment/{payment_id}", response_model=PaymentResponse)
async def get_payment_by(
    payment_id: str,
    service: PaymentService = Depends(get_payment_service)
):
    """"""
    return await service.get_payment_by_id(payment_id)


@router.get("/payment/{column_name}", response_model=List[PaymentResponse])
async def get_all_payments_by(
    column_name: str,
    value: Any,
    service: PaymentService = Depends(get_payment_service)
):
    """"""
    return await service.get_all_payments_by(column_name, value)
