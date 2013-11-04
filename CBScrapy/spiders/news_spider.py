from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image

from CBScrapy.items import NewsItem
class NewsSpider(BaseSpider):
  name = "news"
  allowed_domains= ["cbsnews.com"]
  start_urls = []
  string_ex = "http://www.cbsnews.com/1770-5_162-0-($!$).html?query=politics&searchtype=cbsSearch&sort=updateDate%20desc&rpp=30&pageType=30"
  for i in range(400):
    start_urls.append(string_ex.replace("($!$)", str(i+1)))
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = []
    for i in range(30):
      item = NewsItem()
      selector = '//li[@section=##]&*'
      selector = selector.replace('##', str(i + 1))
      try:
        item['headline'] = hxs.select(selector.replace('&*', '//a[@class="title"]/text()')).extract()[0]
      except IndexError:
        {}
      try:
        item['imgsrc'] = hxs.select(selector.replace('&*', '//img[contains(@class, "storyImg")]/@src')).extract()[0].replace("_75x56", "_640x480").replace("s.jpg", ".jpg")
        #fd = cStringIO.StringIO(urllib.urlopen(item['imgsrc']).read())
        #im = Image.open(fd)
        item['imgSize'] = "640x480"
      except IndexError:
        {}
      try:
        item['url'] = hxs.select(selector.replace('&*', '//a[@class = "title"]/@href')).extract()[0]
      except IndexError:
        {}
      try:
        item['date'] = hxs.select(selector.replace('&*', '//span[@class = "date"]/text()')).extract()[0]
      except IndexError:
        {}
      item['src'] = u'CBS'
      items.append(item)
    return items
