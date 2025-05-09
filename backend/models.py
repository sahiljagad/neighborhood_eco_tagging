from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base


class Sighting(Base):
    __tablename__ = "sightings"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)              # name of the uploaded file
    species = Column(String, nullable=True)                # predicted animal type (optional)
    latitude = Column(Float, nullable=False)               # extracted from image
    longitude = Column(Float, nullable=False)              # extracted from image
    timestamp = Column(DateTime(timezone=True), default=func.now())  # when the image was taken or uploaded
