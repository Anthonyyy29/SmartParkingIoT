# app/schemas/parking.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EntryRequest(BaseModel):
    """Schema untuk request masuk kendaraan."""
    plate: str
    source: Optional[str] = "web"  # Dari web atau IoT device

class ExitRequest(BaseModel):
    """Schema untuk request keluar kendaraan."""
    plate: str
    source: Optional[str] = "web"

class TransactionResponse(BaseModel):
    """Schema untuk response data transaksi."""
    id: int
    plate: str
    entry_time: datetime
    exit_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    fee: Optional[float] = None
    status: str

    class Config:
        orm_mode = True  # Bisa return ORM models langsung
