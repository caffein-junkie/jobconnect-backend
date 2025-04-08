from pydantic import BaseModel
from typing import List


class BusinessLocation(BaseModel):
    lat: float
    lng: float


class BusinessResult(BaseModel):
    map_location: BusinessLocation
    shop_location: str = "N/A"
    shop_name: str = "N/A"
    rating: str = "No rating"
    distance_km: float


class SearchParameters(BaseModel):
    search_string: str
    distance_km: float
    user_lat: float
    user_lon: float


class BusinessSearchResults(BaseModel):
    results: List[BusinessResult]
