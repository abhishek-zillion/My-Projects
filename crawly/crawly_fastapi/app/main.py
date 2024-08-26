import logging
from fastapi import FastAPI
from app.routers import walmart
from sqlalchemy.orm import Session
from app.session import Base, SessionLocal
from app.session import engine


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI(
)

# app.include_router(register.router, prefix="/auth", tags=["Authentication"])
app.include_router(walmart.scrape_walmart,
                   prefix="/all-products", tags=["All Products"])

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    '''
    To run this script,
    python3 -m app.main
    '''
    db = SessionLocal()
    db.close()
    logging.info("Sample data has been saved")
