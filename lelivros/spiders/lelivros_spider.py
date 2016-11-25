from lelivros.notify import EmailNotification
from scrapy.utils.project import data_path
from scrapy import signals, Spider
from scrapy.http import Request
import re

class LeLivrosSpider(Spider):
    name = "lelivros_spider"
    start_urls = ['http://lelivros.top/book/page/1/']

    def __init__(self, emails=None, change_url=None, *args, **kwargs):
        super(LeLivrosSpider, self).__init__(*args, **kwargs)
        self.insert_url = change_url

        if emails is None:
            emails = str()
        self.addresses = re.split('[,\s]+', emails)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LeLivrosSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_opened(self):
        s = self.settings
        self.email = EmailNotification(s['EMAIL'], s['PASSWORD'])
        for address in self.addresses:
            self.email.add_address(address)

        self.path = data_path(s['FILE_NAME'])
        try:
            with open(self.path, 'r') as f:
                self.last_url = f.read()
        except Exception:
            self.last_url = 'URL_NULL'

    def parse(self, response):
        if self.insert_url is not None:
            self.change_url()
        else:
            url = response.url
            last_page = False

            base_xpath = "//ul[contains(@class, 'products')]/li/a[1]/"
            descs = response.xpath(base_xpath + "h3/text()").extract()
            urls = response.xpath(base_xpath + "@href").extract()

            if self.get_page_number(url) == 1:
                self.new_last_url = urls[0].split('/')[-2]

            for book in zip(descs, urls):
                if self.last_url not in book[1]:
                    self.email.add_book(book)
                else:
                    last_page = True
                    break

            if not last_page:
                if response.xpath("//a[contains(@class, 'last')]/@href").extract():
                    yield Request(url=self.get_next_url(url))

    def change_url(self):
        new_data = self.insert_url.split('/')[-2]

        try:
            with open(self.path, 'r') as f:
                old_data = f.read()
        except Exception:
            old_data = 'None'

        with open(self.path, 'w') as f:
            f.write(new_data)

        self.logger.info('Previous data: ' + old_data)
        self.logger.info('New data: ' + new_data)

    def get_page_number(self, url):
        match = re.search(r'\d+', url)

        if match is not None:
            num = int(match.group(0))
        else:
            num = 1

        return num

    def get_next_url(self, url):
        num = self.get_page_number(url)

        if re.search(r'\d+', url) is None:
            url = self.start_urls[0]
        url = re.sub(r'\d+', str(num + 1), url)

        return url

    def spider_closed(self, reason):
        if self.insert_url is None:
            with open(self.path, 'w') as f:
                f.write(self.new_last_url)
            self.email.send()
