from collections import defaultdict
from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from .models import CropLand, CropLocation
from .schemas import LandUpdate, SaveCropFormRequest


async def save_crop_form(data: SaveCropFormRequest, db: AsyncSession):
    # Step 1: Check if location already exists
    result = await db.execute(
        select(CropLocation).where(
            CropLocation.user_id == data.user_id,
            CropLocation.location_name == data.location,
        )
    )
    location_entry = result.scalars().first()

    # Step 2: Create it only if it doesn't exist
    if not location_entry:
        location_entry = CropLocation(user_id=data.user_id, location_name=data.location)
        db.add(location_entry)
        await db.flush()  # get location_entry.id

    # Step 3: Add lands to existing/new location
    for land in data.lands:
        db.add(
            CropLand(
                location_id=location_entry.id,
                area_acres=land.area_acres,
                seed_quantity_kg=land.seed_quantity_kg,
                chemical_recommendation=land.chemical_recommendation,
            )
        )

    await db.commit()


async def get_crop_history(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(CropLocation)
        .where(CropLocation.user_id == user_id)
        .options(selectinload(CropLocation.lands))
    )
    locations = result.scalars().all()

    # Use defaultdict to group by city
    grouped = defaultdict(list)

    for loc in locations:
        for land in loc.lands:
            grouped[loc.location_name].append(
                {
                    "id": land.id,
                    "area_acres": land.area_acres,
                    "seed_quantity_kg": land.seed_quantity_kg,
                    "chemical_recommendation": land.chemical_recommendation,
                    "days_tracked": land.created_at,
                }
            )

    # Return one entry per city
    return [{"location": loc, "lands": lands} for loc, lands in grouped.items()]


async def delete_lands(land_ids: List[int], db: AsyncSession):
    if not land_ids:
        raise HTTPException(status_code=400, detail="No land IDs provided.")
    await db.execute(delete(CropLand).where(CropLand.id.in_(land_ids)))
    await db.commit()


async def update_land(land_id: int, data: LandUpdate, db: AsyncSession):
    result = await db.execute(
        update(CropLand)
        .where(CropLand.id == land_id)
        .values(
            area_acres=data.area_acres,
            seed_quantity_kg=data.seed_quantity_kg,
            chemical_recommendation=data.chemical_recommendation,
        )
        .execution_options(synchronize_session="fetch")
    )
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Land not found.")
    await db.commit()
