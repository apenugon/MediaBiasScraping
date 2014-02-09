from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from CBScrapy.items import NewsItem

class SFCSpider(CrawlSpider):
  name = "slate"
  allowed_domains= ["www.slate.com"]
  start_urls=[]
  string_ex = "http://www.slate.com/articles/news_and_politics.(!y!).html"
  #offset=25440 max
  for i in range(350):
    start_urls.append(string_ex.replace("(!y!)", str(i + 1)))
  rules = (
      Rule(SgmlLinkExtractor(allow=("/articles/")), callback="parse1", follow=False),
  )

  def parse1(self, response):
    hxs = HtmlXPathSelector(response)
    item = NewsItem()
    item['headline'] = hxs.select('//*[@id="ogtitle"]/@content').extract()[0]
    item['url'] = response.url
    item['date'] = hxs.select('//*[@id="article_header"]/div[1]/div[4]/text()').extract()[0]
    try:
      item['imgsrc'] = hxs.select('/html/body/div[2]/article/section/div[2]/div[1]/figure/img/@src').extract()[0]
      item['imgSize'] = '590x421'
    except IndexError:
      {}
    item['src'] = "Slate"

    return item
