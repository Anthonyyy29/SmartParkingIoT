from fastapi import APIRouter
from datetime import datetime, timedelta
from models.schemas import ParkingStatusResponse, VehicleStatus, ErrorResponse, LastTransactionResponse
from database_connection import db
from utils.pricing import calculate_parking_fee

router = APIRouter(prefix="/api", tags=["Admin"])


@router.get(
    "/parking-status",
    response_model=ParkingStatusResponse,
    summary="Get current parking status",
    description="Get list of all vehicles currently parked in the lot"
)
async def get_parking_status():
    """
    Get all vehicles currently in the parking lot (status = 'IN').
    Calculates real-time duration and fee for each vehicle.
    """
    
    query = """
        SELECT id, uid, entry_time, status
        FROM parking_transactions
        WHERE status = 'IN'
        ORDER BY entry_time ASC
    """
    
    transactions = db.execute_query(query)
    
    vehicles = []
    current_time = datetime.now()
    
    if transactions:
        for trans in transactions:
            entry_time = trans['entry_time']
            duration_delta = current_time - entry_time
            duration_minutes = int(duration_delta.total_seconds() / 60)
            
            # Minimum 1 minute
            if duration_minutes <= 0:
                duration_minutes = 1
            
            fee = calculate_parking_fee(duration_minutes)
            
            vehicles.append(VehicleStatus(
                uid=trans['uid'],
                entry_time=entry_time,
                duration_minutes=duration_minutes,
                fee=fee
            ))
    
    return {
        "success": True,
        "active_vehicles": len(vehicles),
        "vehicles": vehicles
    }


@router.get(
    "/last-transaction/{uid}",
    response_model=LastTransactionResponse,
    responses={
        404: {"model": ErrorResponse}
    },
    summary="Get last transaction for a vehicle",
    description="Get the most recent transaction (entry or exit) for a specific vehicle UID"
)
async def get_last_transaction(uid: str):
    """
    Get the last transaction for a specific vehicle UID.
    
    - **uid**: RFID UID of the vehicle
    """
    
    uid = uid.strip()
    if not uid:
        return {
            "success": False,
            "error": "UID cannot be empty",
            "code": "INVALID_UID"
        }
    
    query = """
        SELECT uid, entry_time, exit_time, duration_minutes, fee, status
        FROM parking_transactions
        WHERE uid = %s
        ORDER BY entry_time DESC
        LIMIT 1
    """
    
    transaction = db.execute_query(query, (uid,))
    
    if not transaction:
        return {
            "success": False,
            "error": "No transaction found for this vehicle",
            "code": "NOT_FOUND"
        }
    
    trans = transaction[0]
    
    return {
        "success": True,
        "uid": trans['uid'],
        "entry_time": trans['entry_time'],
        "exit_time": trans['exit_time'],
        "duration_minutes": trans['duration_minutes'],
        "fee": trans['fee'],
        "status": trans['status']
    }
