from pydantic import BaseModel


class PredictRequest(BaseModel):
    evapotranspiration_mm: float
    mean_sea_level_pressure_hpa: float
    mean_soil_moisture: float
    mean_soil_moisture_available: float
    mean_relative_humidity_percent: float
    min_temperature_c: float
    mean_soil_temperature_c: float
    actual_yield: float  # Include only if required by model


class PredictResponse(BaseModel):
    prediction: float
