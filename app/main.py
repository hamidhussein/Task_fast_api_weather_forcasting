from fastapi import FastAPI
from .routers import auth as auth_router
from .routers import weather as weather_router

# Initialize the FastAPI app
app = FastAPI(title="Task_fast_api_weather_forecasting", version="1.0.0")

# Include the auth and weather routers (APIs)
app.include_router(auth_router.router)
app.include_router(weather_router.router)

# Health check endpoint
@app.get("/", tags=["meta"])
def root():
    return {"name": "Task_fast_api_weather_forecasting", "status": "ok"}
