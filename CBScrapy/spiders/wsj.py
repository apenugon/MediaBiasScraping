from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from CBScrapy.items import NewsItem

class SFCSpider(BaseSpider):
  name = "wsj"
  allowed_domains= ["online.wsj.com"]
  start_urls=[]
  string_ex = "http://online.wsj.com/search/term.html?KEYWORDS=Politics&page_no=(!y!)&fromDate=02/12/10&toDate=02/8/14&media=Articles&sort_by=date"
  #offset=25440 max
  for i in range(1300):
    start_urls.append(string_ex.replace("(!y!)", str(i + 1)))
  #rules = (
  #    Rule(SgmlLinkExtractor(allow="/article/"), callback="parse1", follow=False),
  #)

  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = []
    myStuff = hxs.select('/html/body/div[1]/div[2]/div/div[1]/div[3]/ul/li')
    
    for i in myStuff:
      item = NewsItem()
      item['url'] = i.select(".//a/@href").extract()[0]
      item['headline'] = i.select(".//h2/a/text()").extract()[0]
      item['date'] = i.select("./div/ul/li/text()").extract()[0]

      try:
        item['imgsrc'] = i.select("./div/div[@class='newsImage']/a/img/@src").extract()[0]
        item['imgSize'] = "640x360"
      except IndexError:
        {}
      item['src'] = "Wall Street Journal"
      items.append(item)

    return items
    """hxs = HtmlXPathSelector(response)
    item = NewsItem()
    item['headline'] = hxs.select('/html/head/meta[14]/@content').extract()[0]
    item['url'] = response.url
    item['date'] = hxs.select('/html/head/meta[19]/@content').extract()[0]
    try:
      #s = hxs.select("//*[@class='vidThumb']/@style").extract()[0]
      #m = re.search(r"\(([A-Za-z0-9_]+)\)", s)
      item['imgsrc'] = hxs.select("/html/body/div[1]/div[2]/div[2]/div[1]/article/div[5]/div/dl/dt/img/@src").extract()[0]
      item['imgSize'] = '640x360'
    except IndexError:
      {}
    item['src'] = "Wall Street Journal"

    return item"""
