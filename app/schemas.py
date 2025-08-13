from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Auth
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# Weather
class WeatherDay(BaseModel):
    date: str
    temp_max_c: float | None = None
    temp_min_c: float | None = None
    precipitation_mm: float | None = None
    weathercode: int | None = None

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    start_date: str
    end_date: str
    days: list[WeatherDay]
