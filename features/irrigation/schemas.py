from typing import List
from pydantic import BaseModel


class IrrigationRequest(BaseModel):
    location: str
    land_areas: List[float]
    check_date: str  # e.g., "YYYY-MM-DD"


class IrrigationResult(BaseModel):
    land_number: int
    land_area_acres: float
    irrigation_required: bool
    reason: str
    water_volume_liters: float
    date_checked: str
    location: str
