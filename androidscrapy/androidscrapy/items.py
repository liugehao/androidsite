#coding=utf-8

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from androids.models import Upfile, Archive

class UpfileItem(DjangoItem):
    django_model = Upfile
    purl = Field()
    
    
class ArchiveItem(DjangoItem):
    django_model = Archive
