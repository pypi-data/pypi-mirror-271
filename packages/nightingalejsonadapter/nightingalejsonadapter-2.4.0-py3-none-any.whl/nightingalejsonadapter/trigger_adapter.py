from __future__ import annotations
from pydantic import BaseModel
from typing import List
from datetime import datetime


class Model(BaseModel):
    requestid: str
    globalincidentid: str
    agencyid: int
    incidenttype: str
    resourceid: str
    tasktype: str
    locations: List[Location]
    timestamp: datetime
    comments: str
    status: str
    
    
class Location(BaseModel):
    latitude: float
    longitude: float