from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db

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
