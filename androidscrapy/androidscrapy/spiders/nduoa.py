#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from urlparse import urljoin
import re
from datetime import datetime, timedelta
from scrapy import log
from android import settings
import os
from androidscrapy.items import UpfileItem, ArchiveItem
import hashlib


class NduoaSpider(BaseSpider):
    name = 'nduoa'
    start_urls = ['http://www.nduoa.com/cat2?page=1','http://www.nduoa.com/cat1?page=1']

    def parse(self, response):
        #yield  Request('http://www.nduoa.com/apk/detail/461863', callback=self.parse_item)
        log.msg(response.url,  _level=log.INFO)
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//*[@id="main"]/div[2]/div[2]/div[1]/div/ul/li/div[2]/a/@href').extract():
            yield Request(urljoin(response.url, url), callback=self.parse_item)
        for url in hxs.select('//*[@id="pagination"]/a/@href').re('/cat\d+\?&page=\d+'):
            yield Request(urljoin(response.url, url), callback=self.parse)
            
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        i = ArchiveItem()
        i['title'] = hxs.select('//*/span[@class="title"]/text()').extract()[0]
        i['version']  = hxs.select('//*/span[@class="version"]/text()').extract()[0].lstrip('(').rstrip(')')
        i['category'] = hxs.select('//html/body/div/div/div[4]/span[3]/a/text()').extract()[0]
        i['star']  = len(hxs.select('//*/div[@class="starWrap"]/span[@class="star"]/s[@class="full"]').extract()) + len(hxs.select('//*/div[@class="starWrap"]/span[@class="star"]/s[@class="half"]').extract()) * 0.5
        i['androidversion']  = ' '.join(hxs.select('//*/div[@class="adapt row popup"]/div/p/span/text()').extract())
        i['screen']  = ' '.join(hxs.select('//*/div[@class="resolution row popup"]/div/p/span/text()').extract())
        i['author']  = hxs.select('//*/div[@class="author row"]/span/a/text()').extract()[0]
        i['description']  = ''.join(hxs.select('/html/body/div/div[2]/div[2]/div[2]/div/div[@class="inner"]/*').extract())
        i['hits']  = ''.join(re.findall('\d',hxs.select('/html/body/div/div[2]/div/div/div/div[3]/span[@class="count"]/text()').extract()[0]))
        i['url']  = response.url
        i['up_dt']  = datetime.now().date() - timedelta(int(hxs.select('//*[@id="main"]/div[1]/div[1]/div[7]/em/text()').re('\d+')[0]))
        i['powerconsumption']  = ''.join(hxs.select('//*[@id="main"]/div/div/div/div/span[contains(text(),"%s")]/text()' % u'耗电').extract())
        yield i
        
        for url in hxs.select('//*/div/ul[@class="shotbox"]/li/img/@src').extract():
            yield Request(urljoin(response.url,url), meta=dict(purl=response.url, category=1), callback=self.savefile)
        yield Request(urljoin(response.url, hxs.select('/html/body/div/div[2]/div/div/div/div[@class="icon"]/img/@src').extract()[0]), meta=dict(purl=response.url, category=0), callback=self.savefile)
        yield Request(urljoin(response.url, hxs.select('/html/body/div/div[2]/div[2]/div/div/div[2]/div/a[@class="d_pc_normal"]/@href').extract()[0]), meta=dict(purl=response.url, category=2), callback=self.savefile)

    def savefile(self, response):
        urlhash = hashlib.sha1(response.meta['purl']).hexdigest()
        path = os.path.join(settings.MEDIA_ROOT, urlhash)
        if not os.path.exists(path):  os.mkdir(path)
        filename = response.url.split('/')[-1]
        with open(os.path.join(path,filename), 'wb') as f:
            f.write(response.body)
            
        i = UpfileItem()
        i['purl'] = response.meta['purl']
        i['category'] = response.meta['category']
        i['length'] = len(response.body)
        i['path'] = os.path.join(urlhash,filename)
        if response.meta.has_key('redirect_urls'):
            i['url'] = response.meta['redirect_urls'][0]
        else:
            i['url'] = response.url
        return i

