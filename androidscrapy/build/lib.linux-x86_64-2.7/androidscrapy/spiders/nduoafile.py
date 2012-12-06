#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.http import Request
from androidscrapy.items import UpfileItem
from androids.models import  Upfile
from urlparse import urljoin
from android import settings
import os

#from django.db import transaction


class NduoafileSpider(BaseSpider):
    name = 'nduoafile'
    download_delay = 0.1
        
    def start_requests(self):
        for upfile in Upfile.objects.filter(length=0):
            yield Request(upfile.url, meta=dict(archiveid=upfile.archive_id, category=upfile.category), callback=self.savefile)
                   
    def savefile(self, response):
        path = os.path.join(settings.MEDIA_ROOT,str(response.meta['archiveid']))
        if not os.path.exists(path):  os.mkdir(path)
        filename = response.url.split('/')[-1]
        with open(os.path.join(path,filename), 'wb') as f:
            f.write(response.body)
            
        i = UpfileItem()
        i['archive'] = response.meta['archiveid']
        i['category'] = response.meta['category']
        i['length'] = len(response.body)
        i['path'] = os.path.join(str(response.meta['archiveid']),filename)
        if response.meta.has_key('redirect_urls'):
            i['url'] = response.meta['redirect_urls'][0]
        else:
            i['url'] = response.url
        print i['url'],i['length']
        return i
