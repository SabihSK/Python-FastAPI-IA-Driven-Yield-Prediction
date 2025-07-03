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
        return {"crop_history": []}

    location_file_map = {
        "bahawalnagar": "bahawalnagar",
        "faisalabad": "faisalabad",
        "multan": "multan",
        "rahimyarkhan": "ryk",
        "rahimyar": "ryk",
    }

    # Iterate each location and enrich each land with irrigation result
    for entry in crop_data:
        location_key = entry["location"].lower().replace(" ", "")
        mapped_location = location_file_map.get(location_key)

        if not mapped_location:
            continue  # Skip unknown locations

        land_areas = [land["area_acres"] for land in entry.get("lands", [])]
        check_date = datetime.utcnow().strftime("%Y-%m-%d")

        model = RuleBasedIrrigationModel(mapped_location, land_areas)
        irrigation_results = model.check_irrigation_per_land(check_date)

        # Merge irrigation result into land entries
        for idx, land in enumerate(entry["lands"]):
            if idx < len(irrigation_results):
                result = irrigation_results[idx]
                land.update(
                    {
                        "irrigation_required": result["irrigation_required"],
                        "reason": result["reason"],
                        "water_volume_liters": result["water_volume_liters"],
                        "date_checked": result["date_checked"],
                    }
                )

    return {"crop_history": crop_data}
