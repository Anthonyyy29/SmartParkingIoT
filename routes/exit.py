from fastapi import APIRouter
from datetime import datetime
from models.schemas import ExitRequest, ExitResponse, ErrorResponse
from database_connection import db
from utils.pricing import calculate_parking_fee

router = APIRouter(prefix="/api", tags=["Exit"])


@router.post(
    "/exit",
    response_model=ExitResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Record vehicle exit and calculate fee",
    description="Record when a vehicle exits the parking lot and calculate the parking fee"
)
async def vehicle_exit(request: ExitRequest):
    """
    Record vehicle exit from parking lot and calculate parking fee.
    
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
    
    # Find active transaction with this UID
    query = """
        SELECT id, uid, entry_time, status 
        FROM parking_transactions 
        WHERE uid = %s AND status = 'IN'
        ORDER BY entry_time DESC
        LIMIT 1
    """
    transaction = db.execute_query(query, (uid,))
    
    if not transaction:
        return {
            "success": False,
            "error": "Vehicle not found in parking",
            "code": "NOT_FOUND"
        }
    
    transaction_data = transaction[0]
    transaction_id = transaction_data['id']
    entry_time = transaction_data['entry_time']
    
    # Calculate duration and fee
    exit_time = datetime.now()
    duration_delta = exit_time - entry_time
    duration_minutes = int(duration_delta.total_seconds() / 60)
    
    # Handle edge case: if duration is 0, minimum 1 minute
    if duration_minutes <= 0:
        duration_minutes = 1
    
    fee = calculate_parking_fee(duration_minutes)
    
    # Update transaction with exit info
    update_query = """
        UPDATE parking_transactions
        SET exit_time = %s, duration_minutes = %s, fee = %s, status = 'OUT'
        WHERE id = %s
    """
    result = db.execute_update(update_query, (exit_time, duration_minutes, fee, transaction_id))
    
    if result is not None:
        return {
            "success": True,
            "message": "Vehicle exit recorded successfully",
            "transaction_id": transaction_id,
            "uid": uid,
            "entry_time": entry_time,
            "exit_time": exit_time,
            "duration_minutes": duration_minutes,
            "fee": fee,
            "status": "OUT"
        }
    else:
        return {
            "success": False,
            "error": "Failed to record vehicle exit",
            "code": "DATABASE_ERROR"
        }
