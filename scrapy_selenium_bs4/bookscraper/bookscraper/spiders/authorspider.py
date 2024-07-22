import scrapy
from bookscraper.items import AuthorItem


class AuthorspiderSpider(scrapy.Spider):
    name = "authorspider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {
        'ITEM_PIPELINES': {"bookscraper.pipelines.AuthorPipeline": 400},
        'FEEDS': {
            './quotes_data/author_data.json': {'format': 'json', 'overwrite':
                                               True}
        }
    }

    def parse(self, response):
        author_page_link = response.xpath(
            "//small[@class='author']/following-sibling::a/@href").getall()
        yield from response.follow_all(author_page_link, self.parser_author)

        pagination_links = response.css('li.next a::attr(href)').get()
        if pagination_links:  # check if there is a next page
            yield response.follow(pagination_links, self.parse)

    def parser_author(self, response):
        author_item = AuthorItem()
        author_item['name'] = response.xpath(
            "//h3[@class='author-title']/text()").get(),
        author_item['birthdate'] = response.xpath(
            "//span[@class='author-born-date']/text()").get(),
        author_item['bio'] = response.css(
            ".author-description::text").get()
        yield author_item
