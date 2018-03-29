# -*- coding: utf-8 -*-

# Scrapy settings for spider_book project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_book'

SPIDER_MODULES = ['spider_book.spiders']
NEWSPIDER_MODULE = 'spider_book.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'spider_book (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# LOG_LEVEL = 'ERROR'

DOWNLOAD_TIMEOUT = 3
REDIRECT_ENABLED = False
HTTPERROR_ALLOWED_CODES = [302, 301]

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'spider_book.middlewares.SpiderBookSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     'spider_book.middlewares.MyCustomDownloaderMiddleware': 543,
#     'spider_book.middlewares.HttpProxyMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'spider_book.pipelines.SpiderBookPipeline': 300,
}

# scrapy_redis settings
REDIS_ITEMS_KEY = '%(spider)s:items'
REDIS_ITEMS_SERIALIZER = 'cPickle.dumps'

SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_SERIALIZER = "cPickle"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
REDIS_START_URLS_AS_SET = True
REDIS_URL = 'redis://localhost:6379/4'

# mongodb
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'htf_spider'
MONGO_AUTH = {}

# qidian chapter delete
USELESS_CHAPTER = [u'序', u'楔子']
