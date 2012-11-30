#coding=utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import datetime
from androids.models import Upfile, Archive

from django.db.utils import IntegrityError
 

class DjangoPipeline(object):
    def process_item(self, item, spider):
        if not item.has_key('archive'): return item
        upfile = Upfile(archive=Archive.objects.get(pk=item['archive']),
        pic=item['pic'],
        length=item['length'],
        category=item['category']
        )

        try:
            upfile.save()
        except IntegrityError:
            #raise DropItem("Contains duplicate domain: %s" % item['pic'])
            return item
        
