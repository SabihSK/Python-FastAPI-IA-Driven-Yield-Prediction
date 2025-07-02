import logging
from datetime import datetime, timedelta
from fastapi import HTTPException
import pandas as pd
import os

logging.basicConfig(level=logging.DEBUG)


class RuleBasedIrrigationModel:
    def __init__(self, location, land_areas, weather_data_dir="weather_data/"):
        self.location = location.lower().replace(" ", "_")
        self.land_areas = land_areas
        self.weather_data_dir = weather_data_dir
        self.weather_data = self._load_weather_data()

    def _load_weather_data(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                current_dir, self.weather_data_dir, f"{self.location}.csv"
            )
            df = pd.read_csv(file_path)
            df.rename(columns=lambda x: x.strip(), inplace=True)
            df.columns = [
                col.encode("ascii", "ignore").decode("ascii") for col in df.columns
            ]

            # Detect timestamp column (case-insensitive)
            timestamp_col = next(
                (c for c in df.columns if c.lower() == "timestamp"), None
            )
            if not timestamp_col:
                raise ValueError("No 'Timestamp' column found in CSV.")

            df.rename(columns={timestamp_col: "Timestamp"}, inplace=True)

            # Try to parse timestamp; handle multiple formats
            try:
                df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            except Exception:
                # Handle custom format like 20241101T0000
                df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%Y%m%dT%H%M")

            return df

        except FileNotFoundError:
            raise HTTPException(
                status_code=404, detail=f"Weather file for '{self.location}' not found."
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error loading weather data: {str(e)}"
            )

    def check_irrigation_per_land(self, check_date):
        try:
            if isinstance(check_date, str):
                check_date = datetime.strptime(check_date, "%Y-%m-%d")

            logging.debug(f"Checking irrigation for {check_date}")

            window = self.weather_data[
                (self.weather_data["Timestamp"] >= check_date)
                & (self.weather_data["Timestamp"] <= check_date + timedelta(days=4))
            ]

            if window.empty:
                logging.warning(
                    f"No weather data for {check_date}, "
                    "trying to use most recent data."
                )
                latest_data = self.weather_data[
                    self.weather_data["Timestamp"] <= check_date
                ]
                if latest_data.empty:
                    logging.error("No weather data available at all.")
                    raise HTTPException(
                        status_code=404, detail="No weather data available at all."
                    )
                window = latest_data.tail(1)

            prefix = self.location.title()

            def get_column(df, keyword):
                for col in df.columns:
                    if (
                        col.lower().startswith(f"{prefix.lower()}")
                        and keyword.lower() in col.lower()
                    ):
                        return col
                raise ValueError(f"Column matching '{prefix} {keyword}' not found")

            rain_col = get_column(window, "Precipitation Total")
            temp_col = get_column(window, "Temperature [2 m elevation corrected]")
            et_col = get_column(window, "Evapotranspiration")

            total_rain = window[rain_col].sum()
            max_temp = window[temp_col].max()
            et = window[et_col].sum()
            deficit = et - total_rain

            irrigation_required = False
            reason = ""
            if total_rain > 15:
                reason = (
                    f"Rain forecast ({total_rain:.1f} mm), " "irrigation not needed."
                )
            elif deficit > 20:
                irrigation_required = True
                reason = f"Water deficit of {deficit:.1f} mm. " "Irrigation required."
            elif max_temp > 35:
                irrigation_required = True
                reason = f"High temperature ({max_temp:.1f}°C). " "Irrigation required."

            results = []
            for i, area in enumerate(self.land_areas):
                water_mm = 75 if irrigation_required else 0
                water_liters = water_mm * 4047 * area if irrigation_required else 0
                results.append(
                    {
                        "land_number": i + 1,
                        "land_area_acres": area,
                        "irrigation_required": irrigation_required,
                        "reason": (
                            reason if reason else "No critical condition detected"
                        ),
                        "water_volume_liters": round(water_liters, 2),
                        "date_checked": check_date.strftime("%Y-%m-%d"),
                        "location": self.location.title().replace("_", " "),
                    }
                )

            return results
        except Exception as e:
            logging.error(f"Error while processing irrigation check: {e}")
            raise HTTPException(
                status_code=500, detail="Error processing irrigation check"
            )
