# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class NewsItem(Item):
  headline = Field()
  imgsrc = Field()
  imgSize = Field()
  date = Field()
  src = Field()
  url = Field()
