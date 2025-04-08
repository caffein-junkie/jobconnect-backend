from fastapi import APIRouter, HTTPException, Depends
from app.schemas.search_technician import SearchParameters, BusinessSearchResults
from app.services.search_technician import SearchService

router = APIRouter()

async def get_search_service() -> SearchService:
    return SearchService()


@router.post("/search_nearby_businesses/", response_model=BusinessSearchResults)
async def search_nearby_businesses(
    params: SearchParameters,
    service: SearchService = Depends(get_search_service)
    ):
    try:
        return service.search_nearby(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/get_current_location/")
async def get_user_location(service: SearchService = Depends(get_search_service)):
    try:
        return service.get_current_location()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Location error: {str(e)}")
