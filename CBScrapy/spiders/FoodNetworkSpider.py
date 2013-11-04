from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider


from CBScrapy.items import FoodItem

import re

class FoodNetworkSpider(BaseSpider):
    name = 'foodnetwork'
    allowed_domains = ['foodnetwork.com']
    start_urls = ['http://www.foodnetwork.com/search/delegate.do?fnSearchType=recipe']
    
    
    
    def parse(self, response):
        sel = HtmlXPathSelector(response)
        recipe_pattern = re.compile('/recipes/[\s-]*-recipe/index.html')
        for url in sel.select('//a'):
          if recipe_pattern.search(url.select('/text()').extract()[0]) != None:
            yield Request(url, callback=self.parse_recipe)
            
        for search_Page in sel.select('//a[@class="nextprev"]'):
          if search_Page.select('./text').extract() is 'Next &raquo;':
            yield Request(search_Page('@href').extract(), callback=self.parse_recipe)
            return
            
          
            
        

    def parse_recipe(self, response):

        sel = HtmlXPathSelector(response)
        item = FoodItem()
        
        #Title
        item['Title'] = sel.select('//title/text').extract()
        
        #Timing information
        item['TotalTime'] = sel.select('//meta[@itemprop="totalTime"]/text').extract()
        item['PrepTime'] = sel.select('//meta[@itemprop="prepTime"]/text').extract()
        item['CookTime'] = sel.select('//meta[@itemprop="cookTime"]/text').extract()
        
        #Ingredients
        for ingredient in sel.select('//li[@itemprop="ingredients"]/text'):
          item['Ingredients'].append(ingredient.extract())
        
        #Directions
        directions = sel.select('//div[@itemprop="recipeInstructions"]')
        for direction in directions.select('p/text'):
          item['Directions'].append(direction.extract())
          
        return item
