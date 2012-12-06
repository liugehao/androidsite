# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

   
class UpfileItem(Item):
    archive = Field()
    path = Field()
    length = Field()
    category = Field()
    url = Field()