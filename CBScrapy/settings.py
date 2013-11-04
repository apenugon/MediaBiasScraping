# Scrapy settings for CBScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'CBScrapy'

SPIDER_MODULES = ['CBScrapy.spiders']
NEWSPIDER_MODULE = 'CBScrapy.spiders'

DEPTH_LIMIT = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CBScrapy (+http://www.yourdomain.com)'
