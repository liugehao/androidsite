#coding=utf-8
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from androidscrapy.items import UpfileItem
from androids.models import Archive
from urlparse import urljoin
import androidscrapy.settings
from android import settings
import os
import re
class NduoaSpider(CrawlSpider):
    name = 'nduoa'
    allowed_domains = ['nduoa.com']
    #download_delay = 4
    start_urls = ['http://www.nduoa.com/cat2?page=1']
    
    rules = (
        Rule(SgmlLinkExtractor(allow=r'cat2?page=\d*?$'), callback='parse', follow=True),
        Rule(SgmlLinkExtractor(allow=r'apk/detail/\d*?$'), callback='parse_item', follow=True),
    )
    
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        archive = Archive.objects.filter(url=response.url)
        if not archive: 
            archive = Archive(title = hxs.select('//*/span[@class="title"]/text()').extract()[0],
                version = hxs.select('//*/span[@class="version"]/text()').extract()[0],
                category = hxs.select('//html/body/div/div/div[4]/span[3]/a/text()').extract()[0],
                star = len(hxs.select('//*/div[@class="starWrap"]/span[@class="star"]/s[@class="full"]').extract()),
                androidversion = ' '.join(hxs.select('//*/div[@class="adapt row popup"]/div/p/span/text()').extract()),
                screen = ' '.join(hxs.select('//*/div[@class="resolution row popup"]/div/p/span/text()').extract()),
                author = hxs.select('//*/div[@class="author row"]/span/a/text()').extract()[0],
                description = hxs.select('/html/body/div/div[2]/div[2]/div[2]/div/div[@class="inner"]').extract()[0],
                hits = ''.join(re.findall('\d',hxs.select('/html/body/div/div[2]/div/div/div/div[3]/span[@class="count"]/text()').extract()[0])),
                url = response.url
                )
            archive.save()
            yield Request(urljoin(response.url, hxs.select('/html/body/div/div[2]/div[2]/div/div/div[2]/div/a[@class="d_pc_normal"]/@href').extract()[0]), meta=dict(archiveid=archive.id, category=2), callback=self.savefile)
            yield Request(urljoin(response.url,hxs.select('/html/body/div/div[2]/div/div/div/div[@class="icon"]/img/@src').extract()[0]), meta=dict(archiveid=archive.id, category=0), callback=self.savefile)
            for url in hxs.select('//*/div/ul[@class="shotbox"]/li/img/@src').extract():
                yield Request(urljoin(response.url,url), meta=dict(archiveid=archive.id, category=1), callback=self.savefile)
        
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
        i['pic'] = os.path.join(str(response.meta['archiveid']),filename)
        return i
