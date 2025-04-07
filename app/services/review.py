from typing import Any, List, Optional
from app.schemas.review import ReviewCreate, ReviewInDB, ReviewUpdate, ReviewResponse
from app.repositories.review import ReviewRepository
from app.utils.exceptions import NotFoundException


class ReviewService:

    def __init__(self, repo: ReviewRepository) -> None:
        self.repo = repo

    @staticmethod
    def review_in_db_to_response(review: ReviewInDB) -> ReviewResponse:
        """"""
        return ReviewResponse(
            review_id=review.review_id,
            client_id=review.client_id,
            technician_id=review.technician_id,
            booking_id=review.booking_id,
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at
        )

    async def get_all_reviews(self) -> List[ReviewResponse]:
        """"""
        reviews = await self.repo.get_all_reviews()
        return [ReviewService.review_to_response(r) for r in reviews]
    
    async def get_review_by_id(self, review_id: str) -> Optional[ReviewResponse]:
        """"""
        reviews = await self.repo.get_review_by_id(review_id)
        return [ReviewService.review_to_response(r) for r in reviews]
    
    async def get_all_reviews_by(self, column_name: str, value: Any) -> List[ReviewResponse]:
        """"""
        def reviews_to_responses(reviews: List[ReviewInDB]) -> List[ReviewResponse]:
            """"""
            return [ReviewService.review_in_db_to_response(r) for r in reviews]

        match column_name.lower():
            case "booking_id":
                return reviews_to_responses(await self.repo.get_all_reviews_by_booking_id(value))
            case "client_id":
                return reviews_to_responses(await self.repo.get_reviews_by_client_id(value))
            case "technician_id":
                return reviews_to_responses(await self.repo.get_reviews_by_technician_id(value))
            case _:
                return []
    
    async def create_review(self, review_data: ReviewCreate) -> ReviewResponse:
        """"""
        return await self.repo.create_review(review_data)
    
    async def delete_review(self, review_id: str) -> bool:
        """"""
        return await self.repo.delete_review(review_id)
    
    async def update_review(self, review_id: str, update_data: ReviewUpdate) -> ReviewResponse:
        """"""
        return await self.repo.update_review(review_id, update_data)
