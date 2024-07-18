'''
Command to start scrapy project:
scrapy startproject project_name

scrapy genspider bookspider books.toscrap.com
pip install ipython
scrapy shell
fetch('https://books.toscrape.com/')
response
response.css('article.product_pod')
response.css('article.product_pod').get()
books = response.css('article.product_pod')
len(books)

book_1 = books[0]

book_1.css('h3 a::text').get()
book_1.css('h3 a::text')

book_1.css('.product_price .price_color::text').get()

In [22]: book_1.css('h3 a').get()
Out[22]: '<a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the ...</a>'

In [29]: book_1.css('h3 a').attrib['href']
Out[29]: 'catalogue/a-light-in-the-attic_1000/index.html'

In [35]: book_1.css('.product_price .price_color')
Out[35]: [<Selector query="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' product_price ')]/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' price_color ')]" data='<p class="price_color">£51.77</p>'>]

In [36]: book_1.css('.product_price .price_color').get()
Out[36]: '<p class="price_color">£51.77</p>'

In [3]: response.css('li.next a').attrib
Out[3]: {'href': 'catalogue/page-2.html'}

In [4]: response.css('li.next a').attrib['href']
Out[4]: 'catalogue/page-2.html'

In [7]: response.css('li.next a ::attr("href")').get()
Out[7]: 'catalogue/page-2.html'

n [9]: response.css('.product_page .product_main h1::text').get()
Out[9]: 'The Requiem Red

In [8]: response.css('.product_page .product_main h1::text')
Out[8]: [<Selector query="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' product_page ')]/descendant-or-self::*/*[@class and contains(concat(' ', normalize-space(@class), ' '), ' product_main ')]/descendant-or-self::*/h1/text()" data='The Requiem Red'>]

In [12]: response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding
    ...: -sibling::li[1]/a/text()").get()
Out[12]: 'Young Adult'

In [13]: response.xpath("//div[@id='product_description']/following-sibling::p/t
    ...: ext()").get()
Out[13]: "Patient Twenty-nine.A monster roams the halls of Soothing Hills Asylum. Three girls dead. 29 is endowed with the curse…or gift of perception. She hears messages in music, sees lyrics in paintings. And the corn. A lifetime asylum resident, the orchestral corn music is the only constant in her life.Mason, a new, kind orderly, sees 29 as a woman, not a lunatic. And as his bel Patient Twenty-nine.A monster roams the halls of Soothing Hills Asylum. Three girls dead. 29 is endowed with the curse…or gift of perception. She hears messages in music, sees lyrics in paintings. And the corn. A lifetime asylum resident, the orchestral corn music is the only constant in her life.Mason, a new, kind orderly, sees 29 as a woman, not a lunatic. And as his belief in her grows, so does her self- confidence. That perhaps she might escape, might see the outside world. But the monster has other plans. The missing girls share one common thread...each was twenty-nine's cell mate. Will she be next? ...more"


n [16]: table_rows = response.css('table tr')

2024-07-16 14:46:44 [asyncio] DEBUG: Using selector: EpollSelector
In [17]: table_rows
Out[17]: 
[<Selector query='descendant-or-self::table/descendant-or-self::*/tr' data='<tr>\n            <th>UPC</th><td>f77d...'>,
 <Selector query='descendant-or-self::table/descendant-or-self::*/tr' data='<tr>\n            <th>Product Type</th...'>,
 <Selector query='descendant-or-self::table/descendant-or-self::*/tr' data='<tr>\n                <th>Price (excl....'>,
 <Selector query='descendant-or-self::table/descendant-or-self::*/tr' data='<tr>\n                    <th>Price (i...'>,
 <Selector query='descendant-or-self::table/descendant-or-self::*/tr' data='<tr>\n                    <th>Tax</th>...'>,
 <Selector query='descendant-or-self::table/descendant-or-self::*/tr' data='<tr>\n                <th>Availability...'>,
 <Selector query='descendant-or-self::table/descendant-or-self::*/tr' data='<tr>\n                <th>Number of re...'>]

In [19]: table_rows[1].css('td').get()
Out[19]: '<td>Books</td>'

In [20]: table_rows[1].css('td ::text').get()
Out[20]: 'Books'

In [21]: table_rows[3].css('td ::text').get()
Out[21]: '£22.65'

2024-07-16 14:49:54 [asyncio] DEBUG: Using selector: EpollSelector
In [22]: response.css('p.star-rating').attrib
Out[22]: {'class': 'star-rating One'}

2024-07-16 14:52:11 [asyncio] DEBUG: Using selector: EpollSelector
In [23]: response.css('p.star-rating').attrib['class']
Out[23]: 'star-rating One'

sudo mysql -u root -p
pip install mysql-connector-python
sudo apt-get update
sudo apt-get install pkg-config
sudo apt-get install libmysqlclient-dev
pip install mysqlclient

    # user_agent_list = ['Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    #                    'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
    #                    'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
    #                    ]

yield response.follow(book_url, callback=self.parse_book_page,
                                  headers={"User-Agent":
                                           self.user_agent_list[
                                               random.randint(0, len(self.user_agent_list)-1)
                                               ]})


can define start_urls as method of class
scrapy shell "https://quotes.toscrape.com/page/1/"
In [6]: response.css('title::text').re(r'Quotes.*')
Out[6]: ['Quotes to Scrape']

In [11]: response.xpath("//title/text()").get()
Out[11]: 'Quotes to Scrape'

response.xpath("//div[@class='quote']")
response.css('div.quote')

024-07-17 12:28:55 [asyncio] DEBUG: Using selector: EpollSelector
In [16]: quote_data.xpath(".//span[@class='text']/text()")
Out[16]: [<Selector query=".//span[@class='text']/text()" data='“It is our choices, Harry, that show ...'>]

2024-07-17 12:30:29 [asyncio] DEBUG: Using selector: EpollSelector
In [17]: quote_data.xpath(".//span[@class='text']/text()").get()
Out[17]: '“It is our choices, Harry, that show what we truly are, far more than our abilities.”'

author =  quote_data.xpath(".//small[@class='author']/text()").get()

In [32]:  quote_data.xpath(".//div[@class='tags']/a/text()").getall()
Out[32]: ['abilities', 'choices']


In [5]: response.xpath("//li[@class='next']/a").attrib['href']
Out[5]: '/page/2/'

In [12]: response.xpath("//small[@class='author']/following-sibling::a")[0].attr
    ...: ib['href']
Out[12]: '/author/Albert-Einstein'

In [21]: response.xpath("//small[@class='author']/following-sibling::a/@href").g
    ...: etall()
Out[21]: 
['/author/Albert-Einstein',
 '/author/J-K-Rowling',
 '/author/Albert-Einstein',
 '/author/Jane-Austen',
 '/author/Marilyn-Monroe',
 '/author/Albert-Einstein',
 '/author/Andre-Gide',
 '/author/Thomas-A-Edison',
 '/author/Eleanor-Roosevelt',
 '/author/Steve-Martin']



To understand it better, think of it this way:

@classmethod
def from_crawler(cls, crawler):
    return cls(crawler.settings)
    
Scrapy needs to create your middleware.
It calls ScrapeOpsFakeUserAgentMiddleware.from_crawler(crawler).
This class method creates and returns an instance of your middleware.
Scrapy then uses this instance, calling process_request for each request.

The @classmethod decorator allows from_crawler to be called on the class itself, 
providing a flexible way for Scrapy to create and configure your middleware. 
It's a design pattern that allows for more flexible object creation, 
which is particularly useful in frameworks like Scrapy where 
components need to be dynamically configured and instantiated.

$ pip install scrapy-rotating-proxies

can add in spider yield respons.follow.... meta={"proxy":..}

ROTATING_PROXY_LIST = [
    '43.153.177.137:13220',
    '1170.233.117.44:5678',
   #  '115.127.75.27:7777',
   #  '152.26.229.88:9443'

]
DOWNLOADER_MIDDLEWARES = {
    "bookscraper.middlewares.BookscraperDownloaderMiddleware": 543,
    'bookscraper.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,

}

"""
import urllib
def get_proxy_urls(url):
    payload = {'api_key': '764739eb-12be-4d0e-9242-16f491a685fa'}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urllib.urlencode(payload)
    return proxy_url
"""

BOT_NAME = "bookscraper"
This sets the name of your Scrapy project.

SPIDER_MODULES = ["bookscraper.spiders"]
Tells Scrapy where to look for spider definitions.

NEWSPIDER_MODULE = "bookscraper.spiders"
Specifies where new spiders should be created when using the genspider command.

ROBOTSTXT_OBEY = False
When set to False, Scrapy will ignore robots.txt rules. Be cautious with this setting as it may violate website policies.

CONCURRENT_REQUESTS = 32 (commented out)
If uncommented, this would set the maximum number of concurrent requests Scrapy will perform.

DOWNLOAD_DELAY = 3 (commented out)
If uncommented, this would add a delay between requests to the same website to be more polite to the server.

CONCURRENT_REQUESTS_PER_DOMAIN = 16 (commented out)
If uncommented, this would limit the number of concurrent requests to each domain.
CONCURRENT_REQUESTS_PER_IP = 16 (commented out)
Similar to the above, but limits based on IP address instead of domain.

COOKIES_ENABLED = False (commented out)
If uncommented and set to False, this would disable cookie handling.

TELNETCONSOLE_ENABLED = False (commented out)
If uncommented, this would disable the telnet console for debugging.
used for debugging Scrapy spiders.

DEFAULT_REQUEST_HEADERS (commented out)
If uncommented, these would be the default headers sent with each request.

EXTENSIONS (commented out)
If uncommented, this would enable or disable Scrapy extensions.

AUTOTHROTTLE_ENABLED = True (commented out)
If uncommented, this would enable the AutoThrottle extension.


AUTOTHROTTLE_START_DELAY = 5 (commented out)
If AutoThrottle is enabled, this sets the initial download delay.


AUTOTHROTTLE_MAX_DELAY = 60 (commented out)
If AutoThrottle is enabled, this sets the maximum download delay.


AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0 (commented out)
If AutoThrottle is enabled, this sets the average number of requests Scrapy should be sending in parallel.


AUTOTHROTTLE_DEBUG = False (commented out)
If uncommented and set to True, this would enable AutoThrottle debugging.


HTTPCACHE_ENABLED = True (commented out)
If uncommented, this would enable HTTP caching.


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
This sets the request fingerprinter implementation to use.


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
This specifies the reactor Twisted should use.

'''
