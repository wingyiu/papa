# -*- coding: utf-8 -*-

MYSQLS = {
    'default': {
        'NAME': 'data_transfer',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}

MONGODBS = {
    'default': {
        'uri': 'mongodb://localhost:27017',
        'db': 'crawl',
    }
}

REDISS = {
    'default': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
    }
}
