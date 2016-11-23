from lelivros.notify import EmailNotification
from scrapy.utils.project import data_path
from scrapy import signals, Spider
from scrapy.http import Request
import re

class LeLivrosNotificationSpider(Spider):
    name = "lelivros_notification"
    start_urls = ['http://lelivros.top/book/page/1/']

    def __init__(self, emails=None, *args, **kwargs):
        super(LeLivrosNotificationSpider, self).__init__(*args, **kwargs)

        if emails is None:
            emails = list()

        self.addresses = re.split('[,\s]+', emails)

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(LeLivrosNotificationSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
    #     crawler.signals.connect(spider.engine_stopped, signal=signals.engine_stopped)
    #     return spider

    # def spider_opened(self):
    #     s = self.settings
    #     self.email = EmailNotification(s['EMAIL'], s['PASSWORD'])
    #
    #     for address in self.addresses:
    #         self.email.add_address(address)
    #
    #     self.path = data_path()
    #     self.logger.info(self.path)

    def parse(self, response):
        self.path = data_path()
        self.logger.info(self.path)

        url = response.url
        # match = re.search(r'\d+', url)
        #
        # base_xpath = "//ul[contains(@class, 'products')]/li/a[1]/"
        # descs = response.xpath(base_xpath + "h3/text()").extract()
        # urls = response.xpath(base_xpath + "@href").extract()
        #
        # if match is not None:
        #     num = int(match.group(0))
        # else:
        #     url = self.start_urls[0]
        #     num = 1
        #
        # for book in zip(descs, urls):
        #     self.email.add_book(book)
        #
        # is_not_last_page = response.xpath("//a[contains(@class, 'last')]/@href")
        #
        # if is_not_last_page.extract():
        #     url = re.sub(r'\d+', str(num + 1), url)
        #     yield Request(url=url)

    # def engine_stopped(self):
    #     pass
