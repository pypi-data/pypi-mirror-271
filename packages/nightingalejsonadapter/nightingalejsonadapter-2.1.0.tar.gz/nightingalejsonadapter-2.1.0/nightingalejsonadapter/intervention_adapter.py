from __future__ import annotations

from typing import List

from pydantic import BaseModel
from datetime import datetime


class DateObserved(BaseModel):
    type: str
    value: datetime


class Action(BaseModel):
    timestamp: datetime
    action: str


class Payload(BaseModel):
    incident_id: str
    user_id: str
    actions: List[Action]


class Model(BaseModel):
    id: str
    type: str
    dateObserved: DateObserved
    payload: Payload
