from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import get_db

router = APIRouter()

@router.post("/sightings/", response_model=schemas.Sighting)
def create_sighting(sighting: schemas.SightingCreate, db: Session = Depends(get_db)):
    db_sighting = models.Sighting(**sighting.dict())
    db.add(db_sighting)
    db.commit()
    db.refresh(db_sighting)
    return db_sighting