from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ============ REQUEST MODELS ============

class EntryRequest(BaseModel):
    uid: str = Field(..., min_length=1, description="RFID UID kendaraan")
    
    class Config:
        json_schema_extra = {
            "example": {"uid": "1A2B3C4D"}
        }


class ExitRequest(BaseModel):
    uid: str = Field(..., min_length=1, description="RFID UID kendaraan")
    
    class Config:
        json_schema_extra = {
            "example": {"uid": "1A2B3C4D"}
        }


# ============ RESPONSE MODELS ============

class SuccessResponse(BaseModel):
    success: bool
    message: str


class ErrorResponse(BaseModel):
    success: bool
    error: str
    code: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Vehicle not found in parking",
                "code": "NOT_FOUND"
            }
        }


class EntryResponse(SuccessResponse):
    transaction_id: int
    entry_time: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Vehicle entry recorded",
                "transaction_id": 1,
                "entry_time": "2025-11-24T14:30:00"
            }
        }


class ExitResponse(SuccessResponse):
    transaction_id: int
    uid: str
    entry_time: datetime
    exit_time: datetime
    duration_minutes: int
    fee: float
    status: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Vehicle exit recorded",
                "transaction_id": 1,
                "uid": "1A2B3C4D",
                "entry_time": "2025-11-24T14:30:00",
                "exit_time": "2025-11-24T15:45:00",
                "duration_minutes": 75,
                "fee": 7000.00,
                "status": "OUT"
            }
        }


class VehicleStatus(BaseModel):
    uid: str
    entry_time: datetime
    duration_minutes: int
    fee: float


class ParkingStatusResponse(BaseModel):
    success: bool
    active_vehicles: int
    vehicles: List[VehicleStatus]
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "active_vehicles": 2,
                "vehicles": [
                    {
                        "uid": "1A2B3C4D",
                        "entry_time": "2025-11-24T14:30:00",
                        "duration_minutes": 45,
                        "fee": 5000.00
                    },
                    {
                        "uid": "5E6F7G8H",
                        "entry_time": "2025-11-24T13:15:00",
                        "duration_minutes": 90,
                        "fee": 7000.00
                    }
                ]
            }
        }


class LastTransactionResponse(BaseModel):
    success: bool
    uid: str
    entry_time: datetime
    exit_time: Optional[datetime]
    duration_minutes: Optional[int]
    fee: Optional[float]
    status: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "uid": "1A2B3C4D",
                "entry_time": "2025-11-24T14:30:00",
                "exit_time": None,
                "duration_minutes": None,
                "fee": None,
                "status": "IN"
            }
        }
