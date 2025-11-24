import mysql.connector
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from db import SessionLocal, engine
import models, crud
from sqlalchemy.orm import Session
from schemas import EntryRequest, ExitRequest, TransactionResponse

# Init database models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dummy data (tes awal)
items = [
    {"id": 1, "name": "Contoh Barang 1", "price": 1000},
    {"id": 2, "name": "Contoh Barang 2", "price": 2000}
]

@app.get("/items")
def get_items():
    return items

# CORS agar PHP & ESP32 bisa akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency Database SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test koneksi database
@app.get("/test-db")
def test_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="smart_parking"
        )
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        db.close()

        return {"status": "connected", "tables": tables}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# =======================
#     API PARKING
# =======================

@app.post("/api/entry")
def entry_vehicle(req: EntryRequest, db: Session = Depends(get_db)):
    tx = crud.create_entry(db, req.plate)
    return {
        "status": "ok",
        "transaction_id": tx.id,
        "entry_time": tx.entry_time
    }

@app.post("/api/exit")
def exit_vehicle(req: ExitRequest, db: Session = Depends(get_db)):
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

@app.get("/api/active")
def get_active_vehicles(db: Session = Depends(get_db)):
    return crud.get_active_transactions(db)

@app.get("/api/history")
def get_history(db: Session = Depends(get_db)):
    return crud.get_history_transactions(db)

@app.get("/api/transactions")
def get_transactions(db: Session = Depends(get_db)):
    tx = db.query(models.ParkingTransaction).all()
    return tx

@app.get("/api/vehicles")
def get_vehicles(db: Session = Depends(get_db)):
    vehicles = db.query(models.Vehicle).all()
    return vehicles

@app.get("/api/rates")
def get_rates(db: Session = Depends(get_db)):
    rates = db.query(models.ParkingRate).all()
    return rates

@app.get("/")
def root():
    return {"message": "Backend FastAPI Smart Parking sudah jalan!"}

