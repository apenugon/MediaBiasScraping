from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from CBScrapy.items import FoodItem
class FoodSpider(CrawlSpider):
  name = "food"
  allowed_domains= ["www.food.com"]
  start_urls = []
  string_ex = "http://www.food.com/recipe-finder/all?pn=(!m!)"
  
  rules = (
    Rule(SgmlLinkExtractor(allow=("/recipe/"), deny=("nutrition")), callback='parse1', follow = True),
      )
  for i in range(20):
    start_urls.append(string_ex.replace("(!m!)", str(i + 1)));
  
  def parse1(self, response):
    hxs = HtmlXPathSelector(response)
    item = FoodItem()
    item['Title'] = hxs.select('//h1[@itemprop="name"]/text()').extract()[0]
    ingredList = hxs.select('//li[@class="ingredient"]//a/text()').extract()
    numList = hxs.select('//span[@class="amount"]/span[@class="value"]/text()').extract()
    typeList = hxs.select('//span[@class="amount"]/span[@class="type"]/text()').extract()
    ingreds = []
    for i in range(len(ingredList)):
      ingreds.append((ingredList[i], numList[i], typeList[i]));
    item['Ingredients'] = ingreds
    item['TotalTime'] = hxs.select("//meta[@itemprop='totalTime']/@content").extract()[0]
    item['PrepTime'] = hxs.select("//meta[@itemprop='prepTime']/@content").extract()[0]
    item['CookTime'] = hxs.select("//meta[@itemprop='cookTime']/@content").extract()[0]
    item['Directions'] = hxs.select("//div[@class='txt']/text()").extract()
    item['Source'] = "Food.com"
    return item
