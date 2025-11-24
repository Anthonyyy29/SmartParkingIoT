# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Sesuaikan user/password/database sesuai XAMPP
DATABASE_URL = "mysql+pymysql://root:@localhost/smart_parking"

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
