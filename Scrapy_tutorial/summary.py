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

'''
