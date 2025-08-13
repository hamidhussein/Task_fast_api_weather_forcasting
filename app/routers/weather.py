from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from ..auth import get_current_user
from ..schemas import WeatherResponse, WeatherDay
from ..config import settings
import httpx

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("", response_model=WeatherResponse)
async def get_week_forecast(
    city: str = Query(..., description="City name for the weather forecast"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    _user = Depends(get_current_user),
):
    base_url = "https://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": settings.weather_api.api_key,
        "q": city,
        "days": 7,  # 7-day forecast
        "aqi": "no",  # You can disable air quality data if you don't need it
        "alerts": "no",  # Disable weather alerts
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(base_url, params=params)
        response.raise_for_status()  # This will raise an exception if the request fails
        data = response.json()

    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"]["message"])

    forecast = data["forecast"]["forecastday"]
    days = []

    for day in forecast:
        days.append(
            WeatherDay(
                date=day["date"],
                temp_max_c=day["day"]["maxtemp_c"],
                temp_min_c=day["day"]["mintemp_c"],
                precipitation_mm=day["day"]["totalprecip_mm"],
                weathercode=day["day"]["condition"]["code"]
            )
        )

    return WeatherResponse(
        latitude=data["location"]["lat"],
        longitude=data["location"]["lon"],
        start_date=forecast[0]["date"],
        end_date=forecast[-1]["date"],
        days=days,
    )
