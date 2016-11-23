from lelivros.spiders.email_sender import EmailNotification
from scrapy.utils.project import data_path
from scrapy import signals, Spider
from scrapy.http import Request
import re

class LelivrosNotificationSpider(Spider):
    name = "lelivros_notification"
    start_urls = ['http://lelivros.top/book/page/1/']

    def __init__(self, *emails):
        self.email = EmailNotification(emails)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LelivrosNotificationSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.engine_stopped, signal=signals.engine_stopped)
        return spider

    def spider_opened(self):
        self.path = data_path()

    def parse(self, response):
        url = response.url
        match = re.search(r'\d+', url)

        base_xpath = "//ul[contains(@class, 'products')]/li/a[1]/"
        descs = response.xpath(base_xpath + "h3/text()").extract()
        urls = response.xpath(base_xpath + "@href").extract()

        if match is not None:
            num = int(match.group(0))
        else:
            url = self.start_urls[0]
            num = 1

        for book in zip(descs, urls):
            self.notification.add_book(book)

        is_not_last_page = response.xpath("//a[contains(@class, 'last')]/@href")

        if is_not_last_page.extract():
            url = re.sub(r'\d+', str(num + 1), url)
            yield Request(url=url)

    def engine_stopped(self):
        pass
