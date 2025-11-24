# app/api/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.db import models
from app.schemas.parking import EntryRequest, ExitRequest
from . import crud

router = APIRouter(prefix="/api", tags=["parking"])

@router.post("/entry")
def entry_vehicle(req: EntryRequest, db: Session = Depends(get_db)):
    """Endpoint untuk mencatat kendaraan masuk."""
    tx = crud.create_entry(db, req.plate)
    return {
        "status": "ok",
        "transaction_id": tx.id,
        "entry_time": tx.entry_time
    }

@router.post("/exit")
def exit_vehicle(req: ExitRequest, db: Session = Depends(get_db)):
    """Endpoint untuk mencatat kendaraan keluar dan hitung biaya."""
    tx = crud.process_exit(db, req.plate)
    
    if not tx:
        raise HTTPException(status_code=404, detail="Active transaction not found")
    
    return {
        "status": "ok",
        "plate": tx.plate,
        "duration_minutes": tx.duration_minutes,
        "fee": float(tx.fee),
        "exit_time": tx.exit_time
    }

@router.get("/active")
def get_active_vehicles(db: Session = Depends(get_db)):
    """Endpoint untuk melihat kendaraan yang masih di parking."""
    return crud.get_active_transactions(db)

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    """Endpoint untuk melihat history kendaraan yang sudah keluar."""
    return crud.get_history_transactions(db)

@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    """Endpoint untuk melihat semua transaksi."""
    return db.query(models.ParkingTransaction).all()

@router.get("/vehicles")
def get_vehicles(db: Session = Depends(get_db)):
    """Endpoint untuk melihat semua kendaraan."""
    return db.query(models.Vehicle).all()

@router.get("/rates")
def get_rates(db: Session = Depends(get_db)):
    """Endpoint untuk melihat tarif parkir."""
    return db.query(models.ParkingRate).all()
