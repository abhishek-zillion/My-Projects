from typing import Any
import scrapy
from crawly_scrap.items import WalmartItem


class WalmartSpider(scrapy.Spider):
    '''
    This spider will only yield URL
    of products
    '''
    name = "walmart"
    allowed_domains = ["walmart.com"]
    # start_urls = [
    #      "https://www.walmart.com/browse/food/snacks-cookies-chips/976759_976787"
    #  ]

    def __init__(self, start_url=None, *args, **kwargs):
        super(WalmartSpider, self).__init__(*args, **kwargs)
        if start_url:
            self.start_urls = [start_url]  # Dynamically set the start URL
        else:
            self.start_urls = []

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.walmart.com',
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        product_links = response.xpath(
            "//div[@data-testid='item-stack']//a[@link-identifier]/@href"
        ).getall()

        print('Total count: %d' % len(product_links))

        if product_links:

            for link in product_links:
                full_url = response.urljoin(link)

                # Create an item and populate its fields
                walmart_item = WalmartItem()
                walmart_item['url'] = full_url

                # Yield the item to pass it to the pipeline
                yield walmart_item

        # Add code here to follow pagination if needed
