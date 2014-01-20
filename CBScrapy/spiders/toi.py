from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO
from PIL import Image
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

from CBScrapy.items import NewsItem
class TOISpider(CrawlSpider):
  name = "toi"
  allowed_domains= ["timesofindia.indiatimes.com"]
  start_urls = []
  string_ex = "http://timesofindia.indiatimes.com/articlelist_lazyload/30359486.cms?curpg=($!$)"

  rules = (
    Rule(SgmlLinkExtractor(allow=("")), callback="parse1", follow=False),
  )

  for i in range(73):
    start_urls.append(string_ex.replace("($!$)", str(i + 1)))
  def parse1(self, response):
    
    hxs = HtmlXPathSelector(response)
        #/div[@class='clearfix']")
    item = NewsItem()
    if len(hxs.select('//*[@id="mod-article-header"]/h1/text()').extract()) > 0:
      #selector = '//li[@section=##]&*'
      #selector = selector.replace('##', str(i + 1))
      try:
        item['headline'] = hxs.select('//*[@id="mod-article-header"]/h1/text()').extract()[0];
      except IndexError:
        {}
      try:
        item['url'] = response.url
      except IndexError:
        {}
      try:
        curdate = hxs.select('//*[@id="mod-article-byline"]/span[3]'/text()).extract()[0]
        item['date'] = re.sub('<[^<]+?>', '', curdate)
      except IndexError:
        {}
      item['src'] = u'Times of India'
    else:
    #selector = '//li[@section=##]&*'
    #selector = selector.replace('##', str(i + 1))
      try:
        item['headline'] = hxs.select('//*[@id="netspidersosh"]/div[1]/div/div[11]/div[1]/span[1]/h1/text()').extract()[0];
      except IndexError:
        {}
    
      try:
        item['url'] = response.url
      except IndexError:
        {}
      try:
        item['imgsrc'] = hxs.select('//*[@id="bellyad"]/div/div[1]/img/@src').extract()[0]
        item['imgSize'] = "300x209"
      except IndexError:
        {}
      try:
        item['date'] = hxs.select('/html/head/meta[1]/@content').extract()[0]
      except IndexError:
        {}
      item['src'] = u'Times of India'
      return item;
