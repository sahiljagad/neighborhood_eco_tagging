from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Sighting(BaseModel):
    filename: str
    species: Optional[str] = None
    latitude: float
    longitude: float
    timestamp: datetime

    class Config: 
       from_attributes = True