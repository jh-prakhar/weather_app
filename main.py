# main.py
import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from geocode import geocode
from weather_client import get_current_weather, get_5day_forecast, aggregate_daily
from schemas import LocationQuery, CreateSavedRequest, SavedRequestOut
import asyncio
from crud import create_saved_request, get_saved_requests, get_saved_request, update_saved_request, delete_saved_request

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Prakhar Jha Weather App Backend")

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/geocode")
async def api_geocode(payload: LocationQuery):
    candidates = geocode(payload.query)
    if not candidates:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"candidates": candidates}

@app.get("/weather")
async def api_weather(lat: float, lon: float):
    # Fetch current + 5day concurrently
    try:
        cur, forecast = await asyncio.gather(
            get_current_weather(lat, lon),
            get_5day_forecast(lat, lon)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    daily = aggregate_daily(forecast)
    return {"current": cur, "forecast_daily": daily}

@app.post("/saved", response_model=SavedRequestOut)
async def api_create_saved(req: CreateSavedRequest, db: Session = Depends(get_db)):
    # 1) geocode input to resolve lat/lon
    candidates = geocode(req.location_input, limit=1)
    if not candidates:
        raise HTTPException(status_code=404, detail="Location not found")
    loc = candidates[0]
    # 2) validate date range - already enforced in pydantic
    # 3) fetch weather snapshot for date range (OpenWeatherMap has historical only in paid; for demo, store current + forecast)
    current = await get_current_weather(loc["lat"], loc["lon"])
    forecast = await get_5day_forecast(loc["lat"], loc["lon"])
    snapshot = {"current": current, "forecast": forecast}
    # create
    payload = type("obj",(object,),{
        "location_input": req.location_input,
        "resolved_name": loc["name"],
        "latitude": loc["lat"],
        "longitude": loc["lon"],
        "date_from": req.date_from,
        "date_to": req.date_to,
        "notes": req.notes
    })
    sr = create_saved_request(db, payload=payload, snapshot=snapshot)
    return sr

@app.get("/saved")
def api_list_saved(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_saved_requests(db, skip=skip, limit=limit)
    return items

@app.get("/saved/{id}", response_model=SavedRequestOut)
def api_get_saved(id: int, db: Session = Depends(get_db)):
    sr = get_saved_request(db, id)
    if not sr:
        raise HTTPException(status_code=404, "Not Found")
    return sr

@app.put("/saved/{id}", response_model=SavedRequestOut)
def api_update_saved(id: int, updates: dict, db: Session = Depends(get_db)):
    # enforce validation in code: allow updates only to notes, date ranges maybe
    if "date_from" in updates and "date_to" in updates and updates["date_to"] < updates["date_from"]:
        raise HTTPException(status_code=400, detail="Invalid date range")
    sr = update_saved_request(db, id, updates)
    if not sr:
        raise HTTPException(status_code=404)
    return sr

@app.delete("/saved/{id}")
def api_delete_saved(id: int, db: Session = Depends(get_db)):
    deleted = delete_saved_request(db, id)
    if not deleted:
        raise HTTPException(status_code=404)
    return {"ok": True}
