# crud.py
from sqlalchemy.orm import Session
from models import SavedRequest
from datetime import datetime

def create_saved_request(db: Session, *, payload, snapshot):
    sr = SavedRequest(
        location_input=payload.location_input,
        resolved_name=payload.resolved_name,
        latitude=payload.latitude,
        longitude=payload.longitude,
        date_from=payload.date_from,
        date_to=payload.date_to,
        snapshot=snapshot,
        notes=payload.notes
    )
    db.add(sr)
    db.commit()
    db.refresh(sr)
    return sr

def get_saved_requests(db: Session, skip=0, limit=100):
    return db.query(SavedRequest).order_by(SavedRequest.created_at.desc()).offset(skip).limit(limit).all()

def get_saved_request(db: Session, id: int):
    return db.query(SavedRequest).filter(SavedRequest.id==id).first()

def update_saved_request(db: Session, id: int, updates: dict):
    sr = get_saved_request(db, id)
    if not sr:
        return None
    for k, v in updates.items():
        setattr(sr, k, v)
    db.commit()
    db.refresh(sr)
    return sr

def delete_saved_request(db: Session, id: int):
    sr = get_saved_request(db, id)
    if not sr:
        return False
    db.delete(sr)
    db.commit()
    return True
