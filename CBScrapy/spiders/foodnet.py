from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

import re
from CBScrapy.items import FoodItem
class FoodSpider(CrawlSpider):
  name = "foodnet"
  allowed_domains= ["www.foodnetwork.com"]
  start_urls = []
  string_ex = "http://www.foodnetwork.com/search/delegate.do?Ntk=site_search&Nr=Record%20Type:Result&N=501&No=(!m!)"
  
  rules = (
      Rule(SgmlLinkExtractor(allow=("/recipes/"), deny=("/reviews/")), callback='parse1', follow = True),
      )
  for i in range(4000):
    start_urls.append(string_ex.replace("(!m!)", str(12 * i)));
  
  def parse1(self, response):
    hxs = HtmlXPathSelector(response)
    item = FoodItem()
    item['Title'] = hxs.select('//h1[@itemprop="name"]/text()').extract()[0]
    ingredList = hxs.select('//li[@itemprop="ingredients"]').extract()
    ingreds = []
    for i in ingredList:
      ingreds.append(re.sub('<[^<]+?>', '', i).replace('\r', ''));
    item['Ingredients'] = ingreds
    item['TotalTime'] = hxs.select("//dd[@class='head fn_duration clrfix']/text()").extract()[0]
    item['PrepTime'] = hxs.select("//dd[@class='clrfix']/text()").extract()[0]
    item['CookTime'] = hxs.select("//dd[@class='clrfix']/text()").extract()[1]
    dlist = hxs.select('//div[@class="fn_instructions"]/p').extract()
    newlist = []
    for i in dlist:
      newlist.append(re.sub('<[^<]+?>', '', i).replace('\r', ''));
    item['Directions'] = newlist
    item['Source'] = "Food Network"
    return item
