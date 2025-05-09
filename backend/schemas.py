from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SightingCreate(BaseModel):
    filename: str
    species: Optional[str] = None
    latitude: float
    longitude: float


class Sighting(BaseModel):
    filename: str
    species: Optional[str] = None
    latitude: float
    longitude: float
    timestamp: datetime

    class Config: 
        orm_mode = True