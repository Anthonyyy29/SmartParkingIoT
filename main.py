import mysql.connector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import engine
from app.db import Base
from app.api.routes import router

# Inisialisasi database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Parking IoT API",
    description="Backend API untuk sistem smart parking berbasis IoT",
    version="1.0.0"
)

# CORS middleware - izinkan akses dari semua origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# ==================
#   HEALTH CHECK
# ==================

@app.get("/")
def root():
    """Endpoint utama untuk test API."""
    return {"message": "Smart Parking IoT API sudah jalan!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    """Endpoint untuk health check."""
    return {"status": "healthy"}

@app.get("/test-db")
def test_db_connection():
    """Test koneksi database."""
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
        
        return {
            "status": "connected",
            "tables": tables,
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

