from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
from .models import Sighting
from .schemas import Sighting as SightingSchema
from .database import get_db
from .model import predict_image
import os

router = APIRouter()

@router.post("/upload/", response_model=SightingSchema)
#why do we need to use async here and what is the asyc def do here?
async def upload_animal_sighting(
    file: UploadFile = File(...), # what does the ... mean?
    latitude: float = 0.0, 
    longitude: float = 0.0, 
    db: Session = Depends(get_db)
):
    file_location = f"uploads/{file.filename}"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    timestamp = datetime.now()
    animal_type = predict_image(file_location)
    print(f"Predicted animal type: {animal_type}")

    sighting = Sighting(
        filename=file.filename,
        species=animal_type,
        latitude=latitude,
        longitude=longitude,
        timestamp=timestamp
    )

    db.add(sighting)
    db.commit()
    db.refresh(sighting) # why do we need to refresh the sighting?

    return sighting

@router.get("/sightings/", response_model=list[SightingSchema])
async def get_all_sightings(db: Session = Depends(get_db)):
    sightings = db.query(Sighting).all()
    return sightings








