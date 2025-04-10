import googlemaps as gm
from math import radians, cos, sin, asin, sqrt
from urllib.request import urlopen
import requests
import json
from typing import List
from app.schemas.search_technician import (
    SearchParameters,
    BusinessResult,
    BusinessSearchResults,
    BusinessLocation,
)
from app.config import settings


class SearchService:
    def __init__(self):
        self.gmaps_client = gm.Client(key=settings.GOOGLE_API_KEY)

    def _kilometer_to_meter(self, km: float) -> int:
        return int(km * 1000)

    def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        return R * c

    def search_nearby(self, params: SearchParameters) -> BusinessSearchResults:
        radius = self._kilometer_to_meter(params.distance_km)
        location = {"lat": params.user_lat, "lng": params.user_lon}

        query_response = self.gmaps_client.places_nearby(
            location=location,
            keyword=params.search_string,
            radius=radius,
        )

        business_list = query_response.get("results", [])
        results: List[BusinessResult] = []

        for business in business_list:
            biz_location = business["geometry"]["location"]
            distance = self._haversine(
                params.user_lat,
                params.user_lon,
                biz_location["lat"],
                biz_location["lng"]
            )
            results.append(BusinessResult(
                map_location=BusinessLocation(**biz_location),
                shop_location=business.get("vicinity", "N/A"),
                shop_name=business.get("name", "N/A"),
                rating=str(business.get("rating", "No rating")),
                distance_km=round(distance, 2)
            ))

        return BusinessSearchResults(results=results)

    def get_current_location(self) -> dict:
        ip_loc_url = 'http://ipinfo.io/json'
        urlopen(ip_loc_url)  # Just to trigger external IP usage
        geo_loc_url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={settings.GEOLOCATION_KEY}"
        response = requests.post(geo_loc_url, json={"considerIp": True})
        location_data = response.json()
        return location_data['location']
