from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.static import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_USER,
)


engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
