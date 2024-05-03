from __future__ import annotations

from pydantic import BaseModel

from datetime import datetime


class DateObserved(BaseModel):
    type: str
    value: datetime


class Payload(BaseModel):
    victim_id: str
    vitals_sensor_id: str
    vitals_sensor_type: str
    respiratory_rate: int
    systolic_blood_pressure: int
    diastolic_blood_pressure: int
    skin_temperature: float
    body_temperature: float
    heart_rate: int
    heart_rate_variability: int
    oxygen_saturation: int
    timestamp: datetime


class Model(BaseModel):
    id: str
    type: str
    dateObserved: DateObserved
    payload: Payload
