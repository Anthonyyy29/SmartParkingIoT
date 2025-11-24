# app/core/config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Sesuaikan dengan kredensial database XAMPP Anda
DATABASE_URL = "mysql+pymysql://root:@localhost/smart_parking"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency untuk database session di FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
