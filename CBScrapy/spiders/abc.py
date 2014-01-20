from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from CBScrapy.items import NewsItem
class FoodSpider(BaseSpider):
  name = "abc"
  allowed_domains= ["abcnews.go.com"]
  start_urls = []
  string_ex = "http://abcnews.go.com/meta/search/results?searchtext=ABC%20News&r=politics,story&sort=date&offset=(!m!)"
  """
  rules = (
    Rule(SgmlLinkExtractor(allow=("/Politics/")), callback='parse1', follow = True),
      )"""
  for i in range(36000/15):
    start_urls.append(string_ex.replace("(!m!)", str(15 * i)));
  
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = []
    articles = hxs.select("//div[@class='result WireStory']")
    for i in articles:
      item = NewsItem()
      item['headline'] = i.select("./a[@class='title']/text()").extract()[0]
      item['url'] = i.select("./a[@class='title']/@href").extract()[0]
      item['date'] = i.select(".//span[@class='date']/text()").extract()[0]
      item['src'] = u'abc'
      try:
        item['imgsrc'] = i.select(".//img/@src").extract()[0].replace("_mw", "")
        item['imgSize'] = "512x329"
      except IndexError:
        {}
      items.append(item);
    return items
