# app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, func
from app.core.config import Base
import enum

class StatusEnum(str, enum.Enum):
    """Status transaksi parking."""
    IN = "IN"        # Kendaraan masuk
    OUT = "OUT"      # Kendaraan keluar
    PAID = "PAID"    # Sudah membayar
    DONE = "DONE"    # Selesai

class ParkingRate(Base):
    """Model untuk tarif parkir."""
    __tablename__ = "parking_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    base_minutes = Column(Integer, nullable=False)  # Durasi dasar (menit)
    base_fee = Column(DECIMAL(10, 2), nullable=False)  # Biaya dasar
    per_minute_fee = Column(DECIMAL(10, 2), nullable=False)  # Biaya per menit tambahan
    created_at = Column(DateTime, server_default=func.now())

class ParkingTransaction(Base):
    """Model untuk transaksi parking."""
    __tablename__ = "parking_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(50), nullable=False, index=True)  # Plat nomor
    entry_time = Column(DateTime, nullable=False)  # Waktu masuk
    exit_time = Column(DateTime, nullable=True)  # Waktu keluar
    duration_minutes = Column(Integer, nullable=True)  # Durasi (menit)
    fee = Column(DECIMAL(10, 2), nullable=True)  # Biaya
    status = Column(Enum(StatusEnum), default=StatusEnum.IN, nullable=False)  # Status
    created_at = Column(DateTime, server_default=func.now())

class Vehicle(Base):
    """Model untuk data kendaraan."""
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(50), unique=True, nullable=False)  # Plat nomor (unik)
    created_at = Column(DateTime, server_default=func.now())
