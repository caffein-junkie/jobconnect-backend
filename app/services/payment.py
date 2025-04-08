from typing import Any, List, Optional
from app.schemas.payment import PaymentCreate, PaymentInDB, PaymentUpdate, PaymentResponse
from app.repositories.payment import PaymentRepository
from app.utils.exceptions import NotFoundException


class PaymentService:

    def __init__(self, repo: PaymentRepository) -> None:
        self.repo = repo
    
    @staticmethod
    def payment_in_db_to_response(payment: PaymentInDB) -> PaymentResponse:
        """"""
        return PaymentResponse(
            booking_id=payment.booking_id,
            client_id=payment.client_id,
            technician_id=payment.technician_id,
            amount=payment.amount,
            payment_method=payment.payment_method,
            payment_status=payment.payment_status,
            payment_id=payment.payment_id,
            transaction_date=payment.transaction_date
        )
    
    async def create_payment(self, payment_data: PaymentCreate) -> PaymentResponse:
        """"""
        return await self.repo.create(payment_data)
    
    async def delete_payment(self, payment_id: str) -> None:
        """"""
        await self.repo.db(payment_id)
    
    async def update_payment(self, payment_id: str, update_data: PaymentUpdate) -> PaymentResponse:
        """"""
        return await self.repo.update(payment_id, update_data)
    
    async def get_all_payments(self) -> List[PaymentResponse]:
        """"""
        payments = await self.repo.get_all_payments()
        return [PaymentService.payment_in_db_to_response(p) for p in payments]
    
    async def get_payment_by_id(self, payment_id: str) -> Optional[PaymentResponse]:
        """"""
        return await self.repo.get_payment_by_id(payment_id)
    
    async def get_all_payments_by(self, column_name: str, value: Any):
        """"""
        def payments_to_responses(payments: List[PaymentInDB]) -> List[PaymentResponse]:
            """"""
            return [PaymentService.payment_in_db_to_response(p) for p in payments]
        
        match column_name.lower():
            case "technician_id":
                return payments_to_responses(await self.repo.get_all_payments_by_technician_id(value))
            case "client_id":
                return payments_to_responses(await self.repo.get_all_payments_by_client_id(value))
            case "booking_id":
                return payments_to_responses(await self.repo.get_all_payments_by_booking_id(value))
            case "payment_status":
                return payments_to_responses(await self.repo.get_all_payments_by_payment_status(value))
            case "payment_method":
                return payments_to_responses(await self.repo.get_all_payments_by_payment_method(value))
            case _:
                return []
