from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image

from CBScrapy.items import NewsItem
class NBCSpider(BaseSpider):
  name = "nbcnews"
  allowed_domains= ["nbcpolitics.nbcnews.com", "firstread.nbcnews.com"]
  start_urls = []
  string_ex = "http://nbcpolitics.nbcnews.com/_nv/more/section/archive?date=20(!y!)/(!m!)"
  firstread_ex = "http://firstread.nbcnews.com/_nv/more/section/archive?date=20(!y!)/(!m!)"
  #go till 66000, so ($!$) = 6600
  for i in range(2):
    start_urls.append(string_ex.replace("(!y!)", str(11)).replace("(!m!)", str(i + 11)))
  
  for i in range(12):
    start_urls.append(string_ex.replace("(!y!)", str(12)).replace("(!m!)", str(i + 1)))
  for i in range(12):
    start_urls.append(string_ex.replace("(!y!)", str(13)).replace("(!m!)", str(i + 1)))
  for j in range(4):
    for i in range(12):
      start_urls.append(firstread_ex.replace("(!y!)", str(j + 10)).replace("(!m!)", str(i + 1)))
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = [] 
    myStuff = hxs.select('//*[@id="vine-t"]/div[2]/div/div[2]/ul/li')

    for i in myStuff:
      item = NewsItem()
      #selector = '//li[@section=##]&*'
      #selector = selector.replace('##', str(i + 1))
      try:
        item['headline'] = i.select('./article/header/h2/a/text()').extract()[0]
      except IndexError:
        {}
      
      try:
        item['imgsrc'] = i.select('.//img/@src').extract()[0]          #fd = cStringIO.StringIO(urllib.urlopen(item['imgsrc']).read())
          #im = Image.open(fd)
        item['imgSize'] = "600x400"
      except IndexError:
        {}
      try:
        item['url'] = i.select('./article/header/h2/a/@href').extract()[0]
      except IndexError:
        {}
      try:
         item['date'] = i.select('./article/header/time/@datetime').extract()[0]
      except IndexError:
          {}
      item['src'] = u'NBC News'
      
      items.append(item)
    return items
