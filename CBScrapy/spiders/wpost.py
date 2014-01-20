from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image

from CBScrapy.items import NewsItem
class WashSpider(BaseSpider):
  name = "wpost"
  allowed_domains= ["www.washingtonpost.com"]
  start_urls = []
  string_ex = "http://www.washingtonpost.com/newssearch/search.html?st=US&submit=Submit&offset=($!$)0&startat=($!$)0&filter=contenttype:%22Article%22&sort=displaydatetime%20desc"
  #go till 66000, so ($!$) = 6600
  for i in range(6600):
    start_urls.append(string_ex.replace("($!$)", str(i)))
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = [] 

    for i in range(1, 11):
      url = hxs.select('//*[@id="search-results"]/li[' + str(i) + ']/h3/a/@href').extract()[0]
      
      if "/politics/" in url:
        item = NewsItem()
      #selector = '//li[@section=##]&*'
      #selector = selector.replace('##', str(i + 1))
        try:
          item['headline'] = hxs.select('//*[@id="search-results"]/li[' + str(i) + ']/h3/a/text()').extract()[0].replace("\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", "")
        except IndexError:
          {}
      
        try:
          item['imgsrc'] = hxs.select('//*[@id="search-results"]/li[' + str(i) + ']/a/img/@src').extract()[0].replace("145x100", "606w")
          #fd = cStringIO.StringIO(urllib.urlopen(item['imgsrc']).read())
          #im = Image.open(fd)
          item['imgSize'] = "606x406"
        except IndexError:
          {}
        try:
          item['url'] = url
        except IndexError:
          {}
        try:
          item['date'] = hxs.select('//*[@id="search-results"]/li[' + str(i) + ']/cite/span/text()').extract()[0]
        except IndexError:
          {}
        item['src'] = u'The Washington Post'
      
        items.append(item)
    return items
