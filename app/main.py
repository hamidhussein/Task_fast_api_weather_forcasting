from fastapi import FastAPI
from .routers import auth as auth_router
from .routers import weather as weather_router

app = FastAPI(title="Task_fast_api_weather", version="1.0.0")

app.include_router(auth_router.router)
app.include_router(weather_router.router)

@app.get("/", tags=["meta"])
def root():
    return {"name": "Task_fast_api_weather", "status": "ok"}
