import math

def calculate_parking_fee(duration_minutes: int) -> float:
    """
    Calculate parking fee based on duration.
    
    Pricing:
    - First 60 minutes: Rp 5.000
    - Each additional hour: Rp 2.000
    
    Examples:
    - 45 minutes = Rp 5.000
    - 60 minutes = Rp 5.000
    - 75 minutes = Rp 7.000 (5000 + 2000)
    - 120 minutes = Rp 7.000
    - 150 minutes = Rp 9.000 (5000 + 2*2000)
    
    Args:
        duration_minutes (int): Duration in minutes
    
    Returns:
        float: Parking fee in Rupiah
    """
    BASE_MINUTES = 60
    BASE_FEE = 5000.00
    PER_HOUR_FEE = 2000.00
    
    if duration_minutes <= 0:
        return 0.0
    
    if duration_minutes <= BASE_MINUTES:
        return BASE_FEE
    
    # Calculate number of additional hours (ceiling division)
    additional_hours = math.ceil((duration_minutes - BASE_MINUTES) / 60)
    
    total_fee = BASE_FEE + (additional_hours * PER_HOUR_FEE)
    
    return total_fee


def get_parking_rate_info() -> dict:
    """Get parking rate information"""
    return {
        "base_minutes": 60,
        "base_fee": 5000.00,
        "per_hour_fee": 2000.00,
        "currency": "IDR"
    }
