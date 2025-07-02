from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db import Base


class CropLocation(Base):
    __tablename__ = "crop_locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    lands = relationship("CropLand", back_populates="location")


class CropLand(Base):
    __tablename__ = "crop_lands"

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("crop_locations.id"))
    area_acres = Column(Float, nullable=False)
    seed_quantity_kg = Column(Float, nullable=False)
    chemical_recommendation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    location = relationship("CropLocation", back_populates="lands")
