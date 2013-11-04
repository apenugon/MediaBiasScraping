from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from CBScrapy.items import NewsItem
class TimeSpider(CrawlSpider):
  name = "time"
  allowed_domains= ["search.time.com"]
  start_urls = []
  string_ex = "http://search.time.com/results.html?No=($!$)&sid=14184767F65B&N=4291662402&Nf=p_date_range%7CBTWN+20100101+20131031&Ns=p_date_range|1&Nty=1"
  
  """rules = (
    Rule(SgmlLinkExtractor(allow=("No=\d00&sid=14184767F65B&N=4291662402&Nf=p_date_range%7CBTWN+20100101+20131031&Ns=p_date_range|1&Nty=1"), deny=("internalid=endeca_dimension")), callback='parse1', follow = True),
      )"""
  for i in range(1740):
    if (15 * i >= 26111):
      break
    start_urls.append(string_ex.replace("($!$)", str(15 * i)))
    
  
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = []
    for i in range(15):
      item = NewsItem()
      selector = '//div[@class="tout"]&*'
      #selector = selector.replace('##', str(i + 1))
      try:
        item['headline'] = hxs.select("//div[@class='tout']/h3/a/text()").extract()[i]
        #item['headline'] = hxs.extract()
        #print hxs.extract()
      except IndexError:
        {}  
      try:
        item['imgsrc'] = hxs.select(selector.replace('&*', '/div[@class="img"]/a/img/@src')).extract()[i].replace("?w=360", "")
        #fd = cStringIO.StringIO(urllib.urlopen(item['imgsrc']).read())
        #im = Image.open(fd)
        item['imgSize'] = "360x240"
      except IndexError:
        {} 
      try:
        item['url'] = hxs.select(selector.replace('&*', '//h3/a/@href')).extract()[i]
      except IndexError:
        {}
      try:
        item['date'] = hxs.select(selector.replace('&*', '//span[@class = "date"]/text()')).extract()[i]
      except IndexError:
        {}
      item['src'] = u'Time'
      items.append(item)
    return items
