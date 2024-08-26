from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import get_db
from utils.walmart_spider_runner import run_walmart_spider

router = APIRouter()


@router.post("/scrape-walmart/{category}")
def scrape_walmart(category: str, subcategory: str,
                   db: Session = Depends(get_db)):
    # Construct the URL dynamically based on input
    url = f"https://www.walmart.com/browse/food/{category}"

    # Run the Scrapy spider with the constructed URL
    run_walmart_spider(url, db)

    return {"message": "Scraping started for " + url}
