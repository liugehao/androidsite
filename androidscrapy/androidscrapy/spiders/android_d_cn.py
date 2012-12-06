#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from androidscrapy.items import UpfileItem
from androids.models import  Upfile
from urlparse import urljoin
from android import settings
import os
from androids.models import Archive, Upfile

#from django.db import transaction


class NduoafileSpider(BaseSpider):
    name = 'android_d_cn'
    allowed_domains = ['android.d.cn']

    download_delay = 1
    def __init__(self):
        self.start_urls= ["http://android.d.cn/game/all_0_all_all_update_%s/" % i for i in range(1,2)]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        for item in hxs.select('//*[@id="list"]/div[1]/div'):
            url = item.select('a/@href').extract()[0]
            star = item.select('a/span[2]/span[3]/span[1]/@class').extract()[0][-1]
            yield Request(urljoin(response.url, url), meta=dict(star=star), callback=self.parse_item)

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        title, version = hxs.select('//*[@id="main"]/div/div/div/div[@class="info_title"]/text()').extract()[0].split(' v')
        
        archive = Archive(title = title,
                version = version,
                category = hxs.select('//*[@id="main"]/div[1]/div[1]/dl/dd[5]/text()').extract()[0].split(u'：')[-1],
                star = response.meta['star'],
                androidversion = ' '.join(hxs.select('//*/div[@class="adapt row popup"]/div/p/span/text()').extract()),
                screen = ' '.join(hxs.select('//*/div[@class="resolution row popup"]/div/p/span/text()').extract()),
                author = hxs.select('//*/div[@class="author row"]/span/a/text()').extract()[0],
                description = ''.join(hxs.select('/html/body/div/div[2]/div[2]/div[2]/div/div[@class="inner"]/*').extract()),
                hits = ''.join(re.findall('\d',hxs.select('/html/body/div/div[2]/div/div/div/div[3]/span[@class="count"]/text()').extract()[0])),
                url = response.url
                )
        #i = UpfileItem()
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return None
