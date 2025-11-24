from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database_connection import db
from config import settings
from routes import entry, exit, admin

# Startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Smart Parking IoT API...")
    db.connect()
    yield
    # Shutdown
    print("🛑 Shutting down...")
    db.disconnect()

# Create FastAPI app
app = FastAPI(
    title="Smart Parking IoT API",
    description="API for IoT-based smart parking system",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(entry.router)
app.include_router(exit.router)
app.include_router(admin.router)


@app.get(
    "/",
    summary="API Status",
    tags=["Health Check"]
)
async def root():
    """Check API status"""
    return {
        "status": "online",
        "service": "Smart Parking IoT API",
        "version": "1.0.0"
    }


@app.get(
    "/health",
    summary="Health Check",
    tags=["Health Check"]
)
async def health_check():
    """Check API and database health"""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
