# schemas.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class LocationQuery(BaseModel):
    query: str

class CreateSavedRequest(BaseModel):
    location_input: str
    date_from: datetime
    date_to: datetime
    notes: Optional[str] = None

    @validator("date_to")
    def to_after_from(cls, v, values):
        if "date_from" in values and v < values["date_from"]:
            raise ValueError("date_to must be after date_from")
        return v

class SavedRequestOut(BaseModel):
    id: int
    location_input: str
    resolved_name: Optional[str]
    latitude: float
    longitude: float
    date_from: datetime
    date_to: datetime
    snapshot: Optional[dict]
    notes: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
