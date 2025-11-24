# app/api/crud.py
from sqlalchemy.orm import Session
from app.db.models import ParkingTransaction, ParkingRate, StatusEnum
from datetime import datetime

def get_current_rate(db: Session) -> ParkingRate:
    """Ambil tarif parkir terbaru dari database."""
    return db.query(ParkingRate).order_by(ParkingRate.id.desc()).first()

def create_entry(db: Session, plate: str) -> ParkingTransaction:
    """Catat kendaraan masuk ke parking."""
    # Cek apakah sudah ada entry IN untuk plat ini (mencegah duplikat)
    existing = db.query(ParkingTransaction).filter(
        ParkingTransaction.plate == plate,
        ParkingTransaction.status == StatusEnum.IN
    ).order_by(ParkingTransaction.entry_time.desc()).first()
    
    if existing:
        return existing  # Return existing jika sudah ada
    
    # Buat transaksi baru
    tx = ParkingTransaction(
        plate=plate,
        entry_time=datetime.utcnow(),
        status=StatusEnum.IN
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def process_exit(db: Session, plate: str) -> ParkingTransaction:
    """Catat kendaraan keluar dan hitung biaya."""
    # Cari transaksi IN terbaru untuk plat ini
    tx = db.query(ParkingTransaction).filter(
        ParkingTransaction.plate == plate,
        ParkingTransaction.status == StatusEnum.IN
    ).order_by(ParkingTransaction.entry_time.desc()).first()
    
    if not tx:
        return None
    
    # Hitung durasi
    now = datetime.utcnow()
    duration = int((now - tx.entry_time).total_seconds() // 60)
    
    # Ambil tarif atau gunakan default
    rate = get_current_rate(db)
    if not rate:
        # Tarif default: 60 menit = Rp5000, setiap menit tambahan Rp100
        BASE_MINUTES = 60
        BASE_FEE = 5000
        PER_MIN_FEE = 100
    else:
        BASE_MINUTES = int(rate.base_minutes)
        BASE_FEE = float(rate.base_fee)
        PER_MIN_FEE = float(rate.per_minute_fee)
    
    # Hitung biaya
    if duration <= BASE_MINUTES:
        fee = BASE_FEE
    else:
        extra = duration - BASE_MINUTES
        fee = BASE_FEE + extra * PER_MIN_FEE
    
    # Update transaksi
    tx.exit_time = now
    tx.duration_minutes = duration
    tx.fee = fee
    tx.status = StatusEnum.OUT
    
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def get_active_transactions(db: Session):
    """Ambil semua kendaraan yang masih di parking (status IN)."""
    return db.query(ParkingTransaction).filter(
        ParkingTransaction.status == StatusEnum.IN
    ).all()

def get_history_transactions(db: Session):
    """Ambil history kendaraan yang sudah keluar."""
    return db.query(ParkingTransaction).filter(
        ParkingTransaction.status != StatusEnum.IN
    ).order_by(ParkingTransaction.id.desc()).all()
