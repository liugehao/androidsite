#coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import datetime
from androids.models import Upfile, Archive

from django.db.utils import IntegrityError
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.core.scheduler import Scheduler

class DjangoPipeline(object):
#    def __init__(self):
#        dispatcher.connect(self.initialize, signals.engine_started)
#        dispatcher.connect(self.finalize, signals.engine_stopped)
#    def initialize(self):    
#        pass
#    def finalize(self):
#        print u'完蛋啦，结束了'

    def process_item(self, item, spider):
        #if not item.has_key('archive'): return item
        upfile = Upfile(archive_id=item['archive'],
        path=item['path'],
        length=item['length'],
        category=item['category']
        )
        upfile.save()
        return item

        
#        try:
#            upfile.save()
#        except IntegrityError:
#            #raise DropItem("Contains duplicate domain: %s" % item['pic'])
#            return item
        
