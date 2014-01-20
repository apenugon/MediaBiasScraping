from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from CBScrapy.items import NewsItem

class SFCSpider(CrawlSpider):
  name = "sfc"
  allowed_domains= ["www.sfchronicle.com"]
  start_urls=[]
  string_ex = "http://www.sfchronicle.com/?controllerName=search&action=search&searchindex=property&view=premium&sort=date&query=''&search=Search&offset=(!y!)"
  #offset=25440 max
  for i in range(23750):
    start_urls.append(string_ex.replace("(!y!)", str(i * 8)))
  rules = (
      Rule(SgmlLinkExtractor(allow=("/politics/"), deny=("/results/")), callback="parse1", follow=False),
  )

  def parse1(self, response):
    hxs = HtmlXPathSelector(response)
    item = NewsItem()
    item['headline'] = hxs.select('//*[@id="content"]/div[1]/div[1]/div/h2/text()').extract()[0]
    item['url'] = response.url
    item['date'] = hxs.select('/html/head/meta[8]/@content').extract()[0]
    try:
      item['imgsrc'] = hxs.select('//*[@id="content"]/div[1]/div[1]/div/div[2]/div/img/@src').extract()[0]
      item['imgSize'] = '717x504'
    except IndexError:
      {}
    item['src'] = "San Francisco Chronicle"

    return item
