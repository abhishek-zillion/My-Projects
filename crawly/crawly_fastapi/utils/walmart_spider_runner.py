from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapper.crawly_scrap.spiders.walmart import WalmartSpider


def run_walmart_spider(start_url, db):
    process = CrawlerProcess(get_project_settings())
    process.crawl(WalmartSpider, start_url=start_url)
    process.start()
