# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Common(scrapy.Item):
    _version = scrapy.Field()
    _ts = scrapy.Field()
    _model = scrapy.Field()


class PriceEntryItem(Common):
    min_price = scrapy.Field()
    max_price = scrapy.Field()
    avg_price = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    lp_id = scrapy.Field()

