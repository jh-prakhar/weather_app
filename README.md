# weather_app
A weather app
# Prakhar Jha Weather App

This is the enhanced setup including `.env`, `Dockerfile`, and `docker-compose.yml` for your weather application.

---

## 📁 Project Structure
```
prakhar-weather-app/
│
├── main.py
├── models.py
├── database.py
├── crud.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

---

## ⚙️ `.env`
```bash
# .env
# App
APP_NAME="Prakhar Jha Weather App"
APP_ENV=development
APP_PORT=8000

# Weather API (OpenWeatherMap example)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Database (PostgreSQL)
POSTGRES_USER=prakhar
POSTGRES_PASSWORD=prakhar123
POSTGRES_DB=weatherdb
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## 🐳 `Dockerfile`
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 🧩 `docker-compose.yml`
```yaml
version: "3.9"

services:
  app:
    build: .
    container_name: prakhar_weather_app
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - .:/app
    restart: always

  db:
    image: postgres:15
    container_name: weather_db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

---

## 🧠 Load Environment Variables in `main.py`
```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

---

## 🚀 Run the App
```bash
# Build containers
docker-compose build

# Run containers
docker-compose up
```
Then go to 👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

✅ You now have a complete **Dockerized FastAPI + PostgreSQL weather app** for Prakhar Jha!

