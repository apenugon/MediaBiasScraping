from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from CBScrapy.items import NewsItem

class NewRepSpider(CrawlSpider):
  name="newrepub"
  allowed_domains= ["www.newrepublic.com"]
  start_urls=[]
  string_ex='http://www.newrepublic.com/tags/politics?page=(!y!)'
  #max = 440
  for i in range(441):
    start_urls.append(string_ex.replace("(!y!)", str(i)))

  rules = (
      Rule(SgmlLinkExtractor(allow="/article/"), callback="parse1", follow=False),
  )

  def parse1(self, response):
    hxs = HtmlXPathSelector(response)
    item = NewsItem()
    item['headline'] = hxs.select('//*[@id="fixed-header-progress-bar-container"]/span[1]/strong/text()').extract()[0]
    item['url'] = response.url
    item['date'] = hxs.select('//*[@id="title-progress-bar-container"]/span[2]/text()').extract()[0]
    item['src'] = u"New Republic"
    try: #if it's a newer article
      item['imgsrc'] = u'www.newrepublic.com' + hxs.select('//*[@class="legacy-image pull-right"]/img/@src').extract()[0]
      item['imgSize'] = u"242x242"
    except IndexError:
      try: #maybe it's an old article?
        item['imgsrc'] = hxs.select('/html/head/meta[12]/@content').extract()[0]
        item['imgSize'] = u"1250x517"
      except IndexError: #no image
        {}
    return item
