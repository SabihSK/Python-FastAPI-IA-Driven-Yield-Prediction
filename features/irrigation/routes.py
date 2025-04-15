from fastapi import APIRouter, Depends
from core.security import api_key_auth  # Optional: secure with API key
from .schemas import IrrigationRequest
from .services import RuleBasedIrrigationModel

router = APIRouter()


@router.post(
    "/check-irrigation",
    summary="Check irrigation requirement per land"
)
async def check_irrigation(
    request: IrrigationRequest,
    _: str = Depends(api_key_auth)
):
    model = RuleBasedIrrigationModel(request.location, request.land_areas)
    results = model.check_irrigation_per_land(request.check_date)
    return results
