from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from CBScrapy.items import NewsItem
class BWeekSpider(CrawlSpider):
  name = "bweek"
  allowed_domains= ["www.businessweek.com"]
  start_urls = []
  string_ex = "http://www.businessweek.com/archive/(!y!)-(!m!)/news/day1.html"
  
  rules = (
    Rule(SgmlLinkExtractor(allow=("day"), deny=("articles", "stories", "videos", "magazine", "management", "lifestyle", "technology", "business-schools")), callback='parse1', follow = True),
      )
  for i in range(2010, 2014):
    for j in range(1, 13):
      repstr = str(j)
      if j < 10:
        repstr = "0" + repstr
      start_urls.append(string_ex.replace("(!y!)", str(i)).replace("(!m!)", repstr))
    
  
  def parse1(self, response):
    hxs = HtmlXPathSelector(response)
    items = []
    test = "//div[@class='column primary']/div[@class='column center']"
    boxes = hxs.select(test + "/h4[@class='box']/text()").extract()
    for i in range(len(boxes)):
      articles = hxs.select(test + "/ul")[i].select("li/span/@class").extract()
      for j in range(len(articles)):
        if articles[j] == u'channel politics_and_policy':
          item = NewsItem()
          item['headline'] = hxs.select(test + "/ul")[i].select("//li/h1/a/text()").extract()[j]
          item['url'] = hxs.select(test + "/ul")[i].select("//li/h1/a/@href").extract()[j]
          item['date'] = boxes[i]
          item['src'] = "BusinessWeek"
          items.append(item)
    return items
