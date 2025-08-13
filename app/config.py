import json
from pathlib import Path
from pydantic import BaseModel

class DBSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

class JWTSettings(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

class WeatherAPISettings(BaseModel):
    api_key: str

class Settings(BaseModel):
    database: DBSettings
    jwt: JWTSettings
    weather_api: WeatherAPISettings

def load_settings(config_path: str | Path = Path(__file__).resolve().parents[1] / "config.json") -> Settings:
    data = json.loads(Path(config_path).read_text())
    return Settings(**data)

settings = load_settings()
