from __future__ import annotations

from pydantic import BaseModel

from datetime import datetime


class DateObserved(BaseModel):
    type: str
    value: datetime


class Payload(BaseModel):
    victimid: str
    incidentid: str
    devicetype: str
    respiratoryrate: float
    systolicbloodpressure: float
    diastolicbloodpressure: float
    temperature: float
    pulserate: float
    heartratevariability: float
    pulseoxymetry: float
    skinmoisture: float
    encounterdatetime: datetime


class Model(BaseModel):
    id: str
    type: str
    dateObserved: DateObserved
    payload: Payload
