from datetime import datetime
from typing import List
from pydantic import BaseModel


class LandInput(BaseModel):
    area_acres: float
    seed_quantity_kg: float
    chemical_recommendation: str


class SaveCropFormRequest(BaseModel):
    user_id: int
    location: str
    lands: List[LandInput]


class LandOut(BaseModel):
    id: int
    area_acres: float
    seed_quantity_kg: float
    chemical_recommendation: str
    days_tracked: int


class LocationOut(BaseModel):
    location: str
    lands: List[LandOut]


class LandUpdate(BaseModel):
    area_acres: float
    seed_quantity_kg: float
    chemical_recommendation: str


class LandDeleteRequest(BaseModel):
    land_ids: List[int]
