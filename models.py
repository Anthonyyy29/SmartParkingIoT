# models.py
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum, func
from db import Base
import enum

class StatusEnum(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    PAID = "PAID"
    DONE = "DONE"  # optional, kalau kamu pakai 'DONE' sebelumnya

class ParkingRate(Base):
    __tablename__ = "parking_rates"
    id = Column(Integer, primary_key=True, index=True)
    base_minutes = Column(Integer, nullable=False)
    base_fee = Column(DECIMAL(10,2), nullable=False)
    per_minute_fee = Column(DECIMAL(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class ParkingTransaction(Base):
    __tablename__ = "parking_transactions"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(50), nullable=False, index=True)
    entry_time = Column(DateTime, nullable=False)
    exit_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    fee = Column(DECIMAL(10,2), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.IN, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    plate = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
