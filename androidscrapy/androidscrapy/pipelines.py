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
    #with DjangoItem
    def process_item(self, item, spider):
        if item.has_key('path'): 
            item['archive'] = Archive.objects.get(url=item['purl'])
        item.save()
        return item
""" #without DjangoItem
    def process_item(self, item, spider):
        if item.has_key('length'):
            Upfile(archive=Archive.objects.get(url=item['purl']),
            path=item['path'],
            length=item['length'],
            category=item['category'],
	        url = item['url']
            ).save()
        if item.has_key('star'):
            Archive(title = item['title'],
                    version =  item['version'],
                    category =  item['category'],
                    star =  item['star'],
                    androidversion =  item['androidversion'],
                    screen =  item['screen'],
                    author =  item['author'],
                    description =  item['description'],
                    hits =  item['hits'],
                    url =  item['url'],
                    up_dt =  item['up_dt'],
                    powerconsumption =  item['powerconsumption'],
                    ).save()
        return item
"""
