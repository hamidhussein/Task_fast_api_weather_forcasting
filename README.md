# Task_fast_api_weather

A small FastAPI project that provides user signup/login with PostgreSQL and a weekly weather forecast using the free [WeatherAPI](https://www.weatherapi.com/).

## 1) Create & activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

## 2) Install dependencies

```bash
pip install -r requirements.txt
```

## 3) Configure database & JWT

Copy `config.json` and edit the credentials:

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "database": "db_weather_forecasting"
  },
  "jwt": {
    "secret_key": "CHANGE_ME_SUPER_SECRET_KEY",
    "algorithm": "HS256",
    "access_token_expire_minutes": 60
  },
  "weather_api": {
    "api_key": "YOUR_WEATHERAPI_KEY"
  }
}
```

> Make sure PostgreSQL is running and the database exists (e.g., `CREATE DATABASE weatherdb;`). Tables are created automatically on first run.

## 4) Run the API

```bash
uvicorn app.main:app --reload
```

- Docs: http://127.0.0.1:8000/docs
- Health: `GET /` → `{"name":"Task_fast_api_weather","status":"ok"}`

## 5) API Endpoints & JSON I/O

### `POST /signup` — Register a user
**Request JSON**
```json
{
  "email": "alice@example.com",
  "password": "Password123!"
}
```
**Response JSON (201)**
```json
{
  "id": "c0a8014e-5a7a-4d0a-9d34-5c9b1b6e2c9d",
  "email": "alice@example.com",
  "created_at": "2025-08-13T12:34:56.789Z"
}
```

**cURL**
```bash
curl -X POST http://127.0.0.1:8000/signup \\
  -H "Content-Type: application/json" \\
  -d '{"email":"alice@example.com","password":"Password123!"}'
```

---

### `POST /login` — Get access token
**Request JSON**
```json
{
  "email": "alice@example.com",
  "password": "Password123!"
}
```
**Response JSON (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**cURL**
```bash
curl -X POST http://127.0.0.1:8000/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"alice@example.com","password":"Password123!"}'
```

---

### `GET /weather` — Weekly forecast (auth required)
**Query params**: `city`, `lat`, `lon`  
**Headers**: `Authorization: Bearer <token>`

**Example Request**
```
GET /weather?city=Lahore&lat=31.5204&lon=74.3587
```

**Response JSON (200)**
```json
{
  "latitude": 31.52,
  "longitude": 74.36,
  "start_date": "2025-08-13",
  "end_date": "2025-08-19",
  "days": [
    {"date":"2025-08-13","temp_max_c":41.2,"temp_min_c":29.1,"precipitation_mm":0.0,"weathercode":1},
    {"date":"2025-08-14","temp_max_c":40.8,"temp_min_c":28.9,"precipitation_mm":0.0,"weathercode":2}
  ]
}
```

**cURL**
```bash
TOKEN="REPLACE_WITH_LOGIN_TOKEN"
curl -G "http://127.0.0.1:8000/weather" \\
  -H "Authorization: Bearer $TOKEN" \\
  --data-urlencode "city=Lahore" \\
  --data-urlencode "lat=31.5204" \\
  --data-urlencode "lon=74.3587"
```

## 6) Freeze dependencies
From the activated venv:
```bash
pip freeze > requirements.txt
```

## 7) Project structure
```text
Task_fast_api_weather/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── auth.py
│       └── weather.py
├── config.json
├── requirements.txt
└── README.md
```



### Notes
- Weather data is powered by WeatherAPI and requires an API key.
- Keep your real `config.json` **out of version control**.
