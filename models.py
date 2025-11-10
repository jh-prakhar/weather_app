# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SavedRequest(Base):
    __tablename__ = "saved_requests"
    id = Column(Integer, primary_key=True, index=True)
    location_input = Column(String, nullable=False)   # raw user input
    resolved_name = Column(String, nullable=True)     # standardized name from geocoder
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=False)
    snapshot = Column(JSON, nullable=True)            # stored weather data (array/object)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
