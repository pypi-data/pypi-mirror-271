from __future__ import annotations

from pydantic import BaseModel


class DateObserved(BaseModel):
    type: str
    value: str


class Payload(BaseModel):
    victimid: str
    name: str
    surname: str
    dateofbirth: str
    age: int
    gender: str
    encounterdatetime: str
    triagestatus: str 
    totalgcs: int 
    dttid: str 
    currentdisposition: int
    incidentid: str
    contamination: bool
    longitude: float
    latitude: float
    chiefcomplaint: str
    chiefcomplaintname: str
    pregnant: bool
    gcseye: int
    gcsverbal: int
    gcsmotor: int
    nickname: str


class Model(BaseModel):
    id: str
    type: str
    dateObserved: DateObserved
    payload: Payload
