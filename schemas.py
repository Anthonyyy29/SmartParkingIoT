# scchemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EntryRequest(BaseModel):
    plate: str
    source: Optional[str] = "web"

class ExitRequest(BaseModel):
    plate: str
    source: Optional[str] = "web"

class TransactionResponse(BaseModel):
    id: int
    plate: str
    entry_time: datetime
    exit_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    fee: Optional[float] = None
    status: str

    class Config:
        orm_mode = True  # memungkinkan return ORM models langsung
