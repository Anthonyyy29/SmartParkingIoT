# crud.py
from sqlalchemy.orm import Session
from models import ParkingTransaction, ParkingRate, Vehicle, StatusEnum
from datetime import datetime
import math

def get_rate(db: Session):
    # ambil rate paling baru
    rate = db.query(ParkingRate).order_by(ParkingRate.id.desc()).first()
    return rate

def create_entry(db: Session, plate: str):
    # Pastikan tidak ada entry yang masih IN untuk plat yang sama (opsional)
    existing = db.query(ParkingTransaction).filter(
        ParkingTransaction.plate == plate,
        ParkingTransaction.status == StatusEnum.IN
    ).order_by(ParkingTransaction.entry_time.desc()).first()
    if existing:
        # kita bisa return existing atau buat new — pilih return existing untuk mencegah duplikat
        return existing

    tx = ParkingTransaction(
        plate=plate,
        entry_time=datetime.utcnow(),
        status=StatusEnum.IN
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def process_exit(db: Session, plate: str):
    # cari transaksi IN terbaru untuk plat
    tx = db.query(ParkingTransaction).filter(
        ParkingTransaction.plate == plate,
        ParkingTransaction.status == StatusEnum.IN
    ).order_by(ParkingTransaction.entry_time.desc()).first()

    if not tx:
        return None

    now = datetime.utcnow()
    duration = int((now - tx.entry_time).total_seconds() // 60)

    rate = get_rate(db)
    # fallback rate default jika belum ada di tabel
    if not rate:
        BASE_MINUTES = 60
        BASE_FEE = 5000
        PER_MIN_FEE = 100
    else:
        BASE_MINUTES = int(rate.base_minutes)
        BASE_FEE = float(rate.base_fee)
        PER_MIN_FEE = float(rate.per_minute_fee)

    if duration <= BASE_MINUTES:
        fee = BASE_FEE
    else:
        extra = duration - BASE_MINUTES
        fee = BASE_FEE + extra * PER_MIN_FEE

    tx.exit_time = now
    tx.duration_minutes = duration
    tx.fee = fee
    tx.status = StatusEnum.OUT

    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

def get_active_transactions(db: Session):
    return db.query(ParkingTransaction).filter(ParkingTransaction.status == StatusEnum.IN).all()

def get_history_transactions(db: Session):
    return db.query(ParkingTransaction).filter(ParkingTransaction.status != StatusEnum.IN).order_by(ParkingTransaction.id.desc()).all()
