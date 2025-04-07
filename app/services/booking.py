from typing import List, Optional, Any
from app.schemas.booking import BookingCreate, BookingInDB, BookingUpdate, BookingResponse, BookingStatus
from app.repositories.booking import BookingRepository
from app.utils.exceptions import NotFoundException


class BookingService:

    def __init__(self, repo: BookingRepository) -> None:
        self.repo = repo
    
    @staticmethod
    def booking_in_db_to_response(booking: BookingInDB) -> BookingResponse:
        """"""
        return BookingResponse(
            client_id=booking.client_id,
            technician_id=booking.client_id,
            service_type=booking.service_type,
            description=booking.description,
            price=booking.price,
            status=booking.status,
            start_date=booking.start_date,
            end_date=booking.end_date
        ) 
    
    async def get_all_bookings(self) -> List[BookingResponse]:
        """"""
        return await self.repo.get_all_bookings()
    
    async def get_booking_by_id(self, booking_id: str) -> Optional[BookingResponse]:
        """"""
        return await self.repo.get_booking_by_id(booking_id)
    
    async def get_all_bookings_by(self, column_name: str, value: Any) -> List[BookingResponse]:
        """"""
        def bookings_to_responses(bookings: List[BookingInDB]) -> List[BookingResponse]:
            """"""
            return [BookingService.booking_in_db_to_response(b) for b in bookings]

        match column_name.lower():
            case "client_id":
                return bookings_to_responses(await self.repo.get_bookings_by_client_id(value))
            case "technician_id":
                return bookings_to_responses(await self.repo.get_bookings_by_technician_id(value))
            case "service_type":
                return bookings_to_responses(await self.repo.get_bookings_by_service_type(value))
            case "status":
                return bookings_to_responses(await self.repo.get_bookings_by_status(value))
            case _:
                return []
    
    async def update_booking(self, booking_id: str, update_data: BookingUpdate) -> BookingResponse:
        """"""
        updated_booking = await self.repo.update_booking(booking_id, update_data)
        return BookingService.booking_in_db_to_response(updated_booking)
    
    async def delete_booking(self, booking_id: str) -> bool:
        """"""
        return await self.repo.delete(booking_id)
    
    async def create_booking(self, booking_data: BookingCreate) -> BookingResponse:
        """"""
        return await self.repo.create(booking_data)
