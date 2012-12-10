#coding=utf-8

import datetime
from androids.models import Upfile, Archive

from django.db.utils import IntegrityError
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.core.scheduler import Scheduler

class DjangoPipeline(object):
    def process_item(self, item, spider):
        if item.has_key('path'):
            return self.process_item_upfile(item,spider)
            
        item.save()
        return item
    def process_item_upfile(self,item,spider):
        item['archive'] = Archive.objects.get(url=item['purl'])
        item.save()
        item['archive'] = item['archive'].id
        return item
