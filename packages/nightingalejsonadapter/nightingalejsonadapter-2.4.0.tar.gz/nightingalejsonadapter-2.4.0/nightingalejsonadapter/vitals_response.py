from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from datetime import datetime


class VitalPredictions(BaseModel):
    HR: float
    RR: float
    SBP: float
    DBP: float
    SPO2: float


class VitalEarlyWarningScore(BaseModel):
    HR: int
    RR: int
    SBP: int
    DBP: int
    SPO2: int

class ProcedureMessage(BaseModel):
    procedureName: str
    predictedInterventionTimestamp: datetime
    message: str


class Prediction(BaseModel):
    timestamp: datetime
    earlyWarningScore: int
    vitalPredictions: VitalPredictions
    vitalEarlyWarningScore: VitalEarlyWarningScore
    shockIndex: float


class Model(BaseModel):
    UUID: str
    timestamp: datetime
    requestId: str
    lastMeasurementTimestamp: datetime
    predictionTimestampId: str
    predictionTimeDeltaMinutes: int
    victimId: str
    procedureMessageCount: int
    procedureMessages: List[ProcedureMessage]
    predictions: List[Prediction]