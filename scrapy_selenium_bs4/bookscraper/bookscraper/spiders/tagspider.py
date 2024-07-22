import os
import scrapy
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings
from twisted.internet import defer


class TagspiderSpider(scrapy.Spider):
    name = "tagspider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['https://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {},
        'FEEDS': {
            './quotes_data/tag_data.json': {'format': 'json', 'overwrite': True}
        }
    }

    def start_requests(self):
        login_url = 'https://quotes.toscrape.com/login'
        yield scrapy.FormRequest(
            url=login_url,
            formdata={'username': 'test', 'password': 'password'},
            callback=self.after_login,
        )

    def after_login(self, response):
        if 'logout' in response.xpath("//a[contains(@href, 'logout')]/@href").get():
            self.logger.info(
                "Successfully logged in. Proceeding to scrape data.")
            yield from self.parse(response)
        else:
            self.logger.error("Login failed. Proceeding without login.")
            yield from self.parse(response)

    def parse(self, response):
        tags_link = response.xpath('//div[@class="tags"]/a/@href').getall()
        yield from response.follow_all(tags_link, self.parse_tag_page)

        pagination_links = response.css('li.next a::attr(href)').get()
        if pagination_links:
            yield response.follow(pagination_links, self.parse)

    def parse_tag_page(self, response):
        tag = response.xpath("//h3/a/text()").get()
        quotes_div = response.xpath("//div[@class='quote']")
        quotes = (quotes_div.xpath(".//span[@class='text']/text()").getall())
        tag_data = {tag: []}
        for quote in quotes:
            tag_data[tag].append(quote.strip())
        yield tag_data

    @defer.inlineCallbacks
    def close(self, reason=None, spider=None, *args, **kwargs):
        settings = get_project_settings()
        mailer = MailSender.from_settings(settings)
        body = "Scraping job finished. Please find the attached data file."
        subject = "Scraping job finished"
        file_path = os.path.join(os.getcwd(), 'quotes_data', 'tag_data.json')

        try:
            with open(file_path, 'rb') as f:
                yield mailer.send(
                    to=["abhishek.zillioninfotech@gmail.com"],
                    subject=subject,
                    body=body,
                    attachs=[("scraped_data.json", "application/json", f)]
                )
            self.logger.info("Email sent successfully")
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")

        try:
            yield defer.maybeDeferred(super().close, spider or self, reason)
        except Exception as e:
            self.logger.error(f"Error in parent close method: {str(e)}")

        self.logger.info("Spider close process completed")
