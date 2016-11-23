from scrapy import Item, Field

class BookItem(Item):
    desc = Field()
    url = Field()
