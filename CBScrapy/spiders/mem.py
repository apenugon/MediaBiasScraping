from scrapy.spider import BaseSpider;
from scrapy.selector import HtmlXPathSelector
import urllib, cStringIO

from CBScrapy.items import NewsItem

class MySpider(BaseSpider):
  name="mem"
  allowed_domains=["thebridge.cmu.edu"]
  start_urls = []
  string_ex = "https://thebridge.cmu.edu/organization/om/roster/members?Direction=Ascending&page=(!y!)"

  for i in range(5):
    start_urls.append(string_ex.replace("(!y!)", str(i + 1)))
  def parse(self, response):
    hxs = HtmlXPathSelector(response)
    items = []
    stuff = hxs.select("/html/body/table/tbody/tr/td[3]/div/a/text()").extract();
    for i in stuff:
      item = NewsItem();
      item['headline'] = i
      items.append(item);

    return items;
