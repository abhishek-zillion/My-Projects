import scrapy
from pathlib import Path
import os


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        # "https://quotes.toscrape.com/page/2/",
    ]
    custom_settings = {
        'ITEM_PIPELINES': {},
        'FEEDS': {
            './quotes_data/quotes_data.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        # saving html pages in directory
        directory = 'quotes_data'
        if not os.path.exists(directory):
            os.makedirs(directory)
        page = response.url.split("/")[-2]
        file_name = f'{directory}/page-{page}.html'
        Path(file_name).write_bytes(response.body)
        self.log(f'saved file {file_name}')

        # saving quote data to directory
        quotes = response.xpath("//div[@class='quote']")

        for quote_data in quotes:
            quote = quote_data.xpath(".//span[@class='text']/text()").get()
            author = quote_data.xpath(
                "..//smalll[@class='author']/text()").get()
            tags = quote_data.xpath(".//div[@class='tags']/a/text()").getall()
            yield {
                'quote': quote,
                'author': author,
                'tags': tags,
            }
        try:
            next_page = response.xpath(".//li[@class='next']/a").attrib['href']
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        except KeyError as e:
            self.log(f"No next page found: {e}")
