from fastapi import APIRouter
from app.schemas.schemas import ProductUrl
import subprocess
router = APIRouter()


@router.post("/scrape-walmart/")
def scrape_walmart(url: ProductUrl):
    subprocess.Popen(["scrapy", "crawl", "walmart",
                     "-a", f"start_url={url.url}"])
    return {"message": f"Scraping started for {url.url} in a separate process"}
