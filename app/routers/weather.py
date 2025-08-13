from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from ..auth import get_current_user
from ..schemas import WeatherResponse, WeatherDay
import httpx

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("", response_model=WeatherResponse)
async def get_week_forecast(
    date: str = Query(..., description="Start date in YYYY-MM-DD"),
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    _user = Depends(get_current_user),
):
    try:
        start = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    end = start + timedelta(days=6)

    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": ["temperature_2m_max","temperature_2m_min","precipitation_sum","weathercode"],
        "timezone": "auto"
    }
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.get(base_url, params=params)
        res.raise_for_status()
        data = res.json()

    daily = data.get("daily", {})
    dates = daily.get("time", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    wcode = daily.get("weathercode", [])

    days = []
    for i, d in enumerate(dates):
        days.append(WeatherDay(
            date=d,
            temp_max_c=tmax[i] if i < len(tmax) else None,
            temp_min_c=tmin[i] if i < len(tmin) else None,
            precipitation_mm=precip[i] if i < len(precip) else None,
            weathercode=wcode[i] if i < len(wcode) else None,
        ))

    return WeatherResponse(
        latitude=data.get("latitude", lat),
        longitude=data.get("longitude", lon),
        start_date=start.isoformat(),
        end_date=end.isoformat(),
        days=days
    )
