from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image

from CBScrapy.items import NewsItem
class NewsSpider(BaseSpider):
  name = "breitbart"
  allowed_domains= ["breitbart.com"]
  start_urls = []
  string_ex = "http://www.breitbart.com/Big-Government?page=($!$)"
  for i in range(650):
    start_urls.append(string_ex.replace("($!$)", str(i)))
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = []
    articleBlocks = hxs.select("//section[@class='list list-blog-roll']/article[@class='story']")
        
        #/div[@class='clearfix']")
    for i in articleBlocks:
      item = NewsItem()
      if len(i.select(".//div[@class='clearfix']").extract()) > 0:
        i = i.select(".//div[@class='clearfix']")
      #selector = '//li[@section=##]&*'
      #selector = selector.replace('##', str(i + 1))
        try:
          item['headline'] = i.select(".//div[@class='grid_9 omega']/h1/a/text()").extract()[0];
        except IndexError:
          {}
      
        try:
          item['imgsrc'] = i.select('.//img/@src').extract()[0].replace("?w=145", "")
          #fd = cStringIO.StringIO(urllib.urlopen(item['imgsrc']).read())
          #im = Image.open(fd)
          item['imgSize'] = "485x342"
        except IndexError:
          {}
        try:
          item['url'] = "www.breitbart.com" + i.select(".//div[@class='grid_3 alpha']/a/@href").extract()[0]
        except IndexError:
          {}
        try:
          item['date'] = i.select('.//span[@class = "story-time"]/text()').extract()[0]
        except IndexError:
          {}
        item['src'] = u'Breitbart'
      
        items.append(item)
      else:
      #selector = '//li[@section=##]&*'
      #selector = selector.replace('##', str(i + 1))
        try:
          item['headline'] = i.select(".//h1/a/text()").extract()[0];
        except IndexError:
          {}
      
        try:
          item['url'] = "www.breitbart.com" + i.select(".//h1/a/@href").extract()[0]
        except IndexError:
          {}
        try:
          item['date'] = i.select('.//span[@class = "story-time"]/text()').extract()[0]
        except IndexError:
          {}
        item['src'] = u'Breitbart'
      
        items.append(item)

    return items
