from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from features.irrigation.services import RuleBasedIrrigationModel

from .schemas import LandDeleteRequest, LandUpdate, LocationOut, SaveCropFormRequest
from .services import delete_lands, get_crop_history, save_crop_form, update_land

router = APIRouter(prefix="/crop", tags=["Crop Management"])


@router.post("/save")
async def save_crop_data(
    payload: SaveCropFormRequest, db: AsyncSession = Depends(get_db)
):
    await save_crop_form(payload, db)
    return {"message": "Crop form saved successfully"}


@router.get("/history/{user_id}", response_model=List[LocationOut])
async def crop_history(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_crop_history(user_id, db)


@router.delete("/lands/delete")
async def delete_crop_lands(
    payload: LandDeleteRequest, db: AsyncSession = Depends(get_db)
):
    await delete_lands(payload.land_ids, db)
    return {"message": "Lands deleted successfully"}


@router.put("/land/update/{land_id}")
async def update_crop_land(
    land_id: int, data: LandUpdate, db: AsyncSession = Depends(get_db)
):
    await update_land(land_id, data, db)
    return {"message": "Land updated successfully"}


@router.get("/history-with-irrigation/{user_id}")
async def crop_history_with_irrigation(
    user_id: int, db: AsyncSession = Depends(get_db)
):
    crop_data = await get_crop_history(user_id, db)

    if not crop_data:
        return {"crop_history": [], "irrigation_check": []}

    land_areas = []
    first_location = None

    for entry in crop_data:
        if not first_location and "location" in entry:
            first_location = entry["location"].lower().replace(" ", "")
        for land in entry.get("lands", []):
            land_areas.append(land.get("area_acres", 0))

    # 🔁 Map location name to file name
    location_file_map = {
        "bahawalnagar": "bahawalnagar",
        "faisalabad": "faisalabad",
        "multan": "multan",
        "rahimyar": "ryk",
        "rahimyarkhan": "ryk",
    }

    mapped_location = location_file_map.get(first_location)
    if not mapped_location:
        raise HTTPException(
            status_code=400, detail=f"Unknown location: {first_location}"
        )

    check_date = datetime.utcnow().strftime("%Y-%m-%d")

    model = RuleBasedIrrigationModel(mapped_location, land_areas)
    irrigation_results = model.check_irrigation_per_land(check_date)

    return {"crop_history": crop_data, "irrigation_check": irrigation_results}
