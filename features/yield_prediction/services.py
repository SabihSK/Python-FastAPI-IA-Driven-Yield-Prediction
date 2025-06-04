import numpy as np

from .loader import models
from .schemas import PredictRequest


def run_prediction(model_key: str, data: PredictRequest) -> float:
    input_data = np.array(
        [
            [
                data.evapotranspiration_mm,
                data.mean_sea_level_pressure_hpa,
                data.mean_soil_moisture,
                data.mean_soil_moisture_available,
                data.mean_relative_humidity_percent,
                data.min_temperature_c,
                data.mean_soil_temperature_c,
                data.actual_yield,
            ]
        ],
        dtype=np.float32,
    )

    # Reshape to match model input: (batch_size, time_steps, features)
    input_data = input_data.reshape((1, 1, 8))

    model = models.get(model_key)
    if model is None:
        raise ValueError(f"Model '{model_key}' not found.")

    prediction = model.predict(input_data)
    return float(prediction[0])
