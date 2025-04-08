from fastapi import APIRouter
from .admin import router as admin_router
from .client import router as client_router
from .technician import router as technician_router
from .booking import router as booking_router
from .review import router as review_router
from .payment import router as payment_router
from .search_technician import router as search_router

router: APIRouter = APIRouter()

router.include_router(admin_router, tags=["Admins"])
router.include_router(client_router, tags=["Clients"])
router.include_router(technician_router, tags=["Technicians"])
router.include_router(booking_router, tags=["Bookings"])
router.include_router(review_router, tags=["Reviews"])
router.include_router(payment_router, tags=["Payments"])
router.include_router(search_router, tags=["Search Technicians"])
