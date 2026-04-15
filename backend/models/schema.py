# backend/models/schema.py

from pydantic import BaseModel

class SensorData(BaseModel):
    temp: float
    humidity: float
    light: float
    air: float
    sound: float
    motion: int
    movement: float