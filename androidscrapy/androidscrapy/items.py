# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from androids.models import Upfile, Archive

class UpfileItem(DjangoItem):
    django_model = Upfile
    purl = Field()
    
    
class ArchiveItem(DjangoItem):
    django_model = Archive
    
""" #without DjangoItem
class UpfileItem(Item):
    archive = Field()
    path = Field()
    length = Field()
    category = Field()
    url = Field()
    purl = Field()

class ArchiveItem(Item):
    title = Field()
    version = Field()
    category = Field()
    star = Field()
    androidversion = Field()
    screen = Field()
    author = Field()
    description = Field()
    hits = Field()
    url = Field()
    up_dt = Field()
    powerconsumption = Field()
"""

