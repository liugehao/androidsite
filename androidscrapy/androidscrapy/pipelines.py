#coding=utf-8

import datetime
from androids.models import Upfile, Archive
#from scrapy import signals
#from scrapy.xlib.pydispatch import dispatcher
#from scrapy.core.scheduler import Scheduler
from django.db import transaction
from scrapy import log

class DjangoPipeline(object):
    #@transaction.commit_on_success
    @transaction.commit_manually
    def process_item(self, item, spider):
        if item.has_key('path'): return self.process_item_upfile(item,spider)
        
        try:
            item.save()
        except:
            transaction.rollback()
            log.msg("(url):%s" % (item['url']), _level=log.ERROR)
        else:
            transaction.commit()
        return item
        
    @transaction.commit_manually
    def process_item_upfile(self,item,spider):
        try:
            item['archive'] = Archive.objects.get(url=item['purl'])
            item.save()
            item['archive'] = item['archive'].id
        except:
            transaction.rollback()
            log.msg("url:%s, [purl]:%s" % (item['url'], item['purl']), _level=log.ERROR)
        else:
            transaction.commit()
        return item
