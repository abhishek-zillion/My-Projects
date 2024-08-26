import scrapy
from crawly_scrap.items import WalmartItem
from crawly_scrap.static import headers as fake_headers


class WalmartSpider(scrapy.Spider):
    '''
    This spider will only yield URL
    of products
    '''
    name = "walmart"
    allowed_domains = ["walmart.com"]

    def __init__(self, start_url=None, *args, **kwargs):
        super(WalmartSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []

    def start_requests(self):
        headers = fake_headers
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

                walmart_item = WalmartItem()
                walmart_item['url'] = full_url

                yield walmart_item

        # To do: code to follow pagination if needed
