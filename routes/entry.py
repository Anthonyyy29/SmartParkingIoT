from fastapi import APIRouter, status
from datetime import datetime
from models.schemas import EntryRequest, EntryResponse, ErrorResponse
from database_connection import db

router = APIRouter(prefix="/api", tags=["Entry"])


@router.post(
    "/entry",
    response_model=EntryResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Record vehicle entry",
    description="Record when a vehicle enters the parking lot via RFID gate"
)
async def vehicle_entry(request: EntryRequest):
    """
    Record vehicle entry to parking lot.
    
    - **uid**: RFID UID of the vehicle (required)
    """
    
    # Validate UID format
    uid = request.uid.strip()
    if not uid:
        return {
            "success": False,
            "error": "UID cannot be empty",
            "code": "INVALID_UID"
        }
    
    if len(uid) > 50:
        return {
            "success": False,
            "error": "UID format too long (max 50 characters)",
            "code": "INVALID_UID_FORMAT"
        }
    
    # Check if vehicle already exists in system
    check_vehicle = "SELECT id FROM vehicles WHERE uid = %s"
    vehicle = db.execute_query(check_vehicle, (uid,))
    
    if not vehicle:
        # Insert new vehicle
        insert_vehicle = "INSERT INTO vehicles (uid) VALUES (%s)"
        db.execute_update(insert_vehicle, (uid,))
    
    # Check if vehicle is already in parking (status = 'IN')
    check_active = "SELECT id FROM parking_transactions WHERE uid = %s AND status = 'IN'"
    active_transaction = db.execute_query(check_active, (uid,))
    
    if active_transaction:
        return {
            "success": False,
            "error": "Vehicle is already in parking",
            "code": "ALREADY_PARKED"
        }
    
    # Insert entry transaction
    entry_time = datetime.now()
    insert_entry = """
        INSERT INTO parking_transactions (uid, entry_time, status)
        VALUES (%s, %s, 'IN')
    """
    transaction_id = db.execute_update(insert_entry, (uid, entry_time))
    
    if transaction_id:
        return {
            "success": True,
            "message": "Vehicle entry recorded successfully",
            "transaction_id": transaction_id,
            "entry_time": entry_time
        }
    else:
        return {
            "success": False,
            "error": "Failed to record vehicle entry",
            "code": "DATABASE_ERROR"
        }
