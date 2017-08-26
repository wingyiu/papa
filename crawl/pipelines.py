# -*- coding: utf-8 -*-
import os
import datetime
import json
from proxy.items import *

import redis
import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class VersionPipeline(object):
    """read version from mysql/redis.file，then add version to items"""
    def __init__(self, settings):
        self.host = settings.get('REDISS')['default']['host']
        self.port = settings.get('REDISS')['default']['port']
        self.db = settings.get('REDISS')['default']['db']
        self.version_key = settings.get('REDIS_VERSION_KEY')
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
        self.version = 1

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            settings=crawler.settings
        )

    def open_spider(self, spider):
        self.version_key = self.version_key % {'name': spider.name, }
        version = self.client.get(self.version_key)
        if not version:
            self.version = 1
            self.client.set(self.version_key, self.version)
        else:
            self.version = int(version.decode('utf-8'))

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['_version'] = self.version
        return item


class TimestampPipeline(object):
    """auto add timestamp to items"""

    def process_item(self, item, spider):
        item['_ts'] = datetime.datetime.utcnow()
        return item


class ModelPipeline(object):
    """auto add item name to items"""

    def process_item(self, item, spider):
        item['_model'] = item.__class__.__name__
        return item


class MongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODBS')['default']['uri'],
            mongo_db=crawler.settings.get('MONGODBS')['default']['db'],
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = spider.name
        self.db[collection_name].insert_one(dict(item))
        return item
