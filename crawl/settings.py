# -*- coding: utf-8 -*-
import os
# Scrapy settings for crawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawl'

SPIDER_MODULES = ['crawl.spiders']
NEWSPIDER_MODULE = 'crawl.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Baiduspider ( http://www.baidu.com/search/spider.htm)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 42

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1  # TODO random delay
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'crawl.middlewares.CrawlSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES_BASE = {
#     'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
#     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
#     'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'middlewares.retry.RetryMiddleware': 550,
    'middlewares.random_proxyredis.RandomProxyMiddleware': 740,
    # 'middlewares.random_proxy.RandomProxyMiddleware': 740,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    # disables the default UserAgentMiddleware and enables the RandomUserAgentMiddleware
    'scrapy.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'middlewares.random_useragent.RandomUserAgentMiddleware': 450,
    'middlewares.downloadtime.DownloadTimeLoggingMiddleware': 800,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'crawl.pipelines.pipelines.VersionPipeline': 300,
    'crawl.pipelines.pipelines.TimestampPipeline': 310,
    'crawl.pipelines.pipelines.ModelPipeline': 320,
    'crawl.pipelines.pipelines.MongoDBPipeline': 330,
    # Store scraped item in redis for post-processing.
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# UA列表，用于随机切换UA
USER_AGENTS_LIST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../useragents/pc.txt')

# 爬虫运行版本记录文件
VERSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Retry many times since proxies often fail
RETRY_TIMES = 10

# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 407, 408, 429]

# default 180s
DOWNLOAD_TIMEOUT = 50

try:
    from crawl.settings_proxy import *
    from crawl.settings_scrapyredis import *
    from crawl.settings_db import *
    from crawl.settings_local import *
except ImportError:
    pass
