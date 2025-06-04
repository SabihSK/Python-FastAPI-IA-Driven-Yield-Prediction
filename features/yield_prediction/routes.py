from fastapi import APIRouter, HTTPException
from .schemas import PredictRequest, PredictResponse
from .services import run_prediction

router = APIRouter(prefix="/yield", tags=["Yield Prediction"])


@router.post("/{location}/predict", response_model=PredictResponse)
def predict(location: str, data: PredictRequest):
    try:
        result = run_prediction(location.lower(), data)
        return PredictResponse(prediction=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
