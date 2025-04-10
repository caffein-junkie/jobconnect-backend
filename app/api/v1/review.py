from typing import List, Any
from fastapi import APIRouter, Request, Depends
from app.schemas.review import ReviewResponse, ReviewCreate, ReviewUpdate
from app.repositories.review import ReviewRepository
from app.services.review import ReviewService
from app.database.database import AsyncDatabase

router: APIRouter = APIRouter()

async def get_db(request: Request) -> AsyncDatabase:
    return request.app.state.db

async def get_review_repository(db: AsyncDatabase = Depends(get_db)) -> ReviewRepository:
    return ReviewRepository(db)

async def get_review_service(repo: ReviewRepository = Depends(get_review_repository)) -> ReviewService:
    return ReviewService(repo)


@router.post("/review", response_model=ReviewResponse)
async def create_review(
    review_data: ReviewCreate,
    service: ReviewService = Depends(get_review_service)
):
    """"""
    return await service.create_review(review_data)


@router.put("/review/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    update_data: ReviewUpdate,
    service: ReviewService = Depends(get_review_service)
):
    """"""
    return await service.update_review(review_id, update_data)


@router.delete("/review/{review_id}")
async def delete_review(
    review_id: str,
    service: ReviewService = Depends(get_review_service)
):
    """"""
    result = service.delete_review(review_id)
    return {"result": result}


@router.get("/review", response_model=List[ReviewResponse])
async def get_all_reviews(service: ReviewService = Depends(get_review_service)):
    """"""
    return await service.get_all_reviews()

@router.get("/review/{review_id}", response_model=ReviewResponse)
async def get_review_by(
    review_id: str,
    service: ReviewService = Depends(get_review_service)
):
    """"""
    return await service.get_review_by_id(review_id)


@router.get("/review/{column_name}", response_model=List[ReviewResponse])
async def get_all_reviews_by(
    column_name: str,
    value: Any,
    service: ReviewService = Depends(get_review_service)
):
    """"""
    return await service.get_all_reviews_by(column_name, value)
