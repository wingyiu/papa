# -*- coding: utf-8 -*-
"""
从快代理拉取代理
"""
import sys
import os
import time
import requests
import redis
import random

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))  #
from proxy.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PROXY_POOL_KEY, REDIS_PROXY_BAD_KEY, REDIS_PROXY_ALIVE_KEY, REDIS_PROXY_DEAD_KEY

url = 'http://svip.kuaidaili.com/api/getproxy/?orderid=978956339172676&num=5000&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_ha=1&sep=2'


def fetch():
    """"""
    client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    r = requests.get(url, )
    lines = r.text.split('\n')
    for line in lines:
        ip, port = line.split(':')
        l = '%s://%s:%s' % ('http', ip, port)
        print(l)
        ism = client.sismember(REDIS_PROXY_DEAD_KEY, l)
        if not ism:
            client.sadd(REDIS_PROXY_POOL_KEY, l)

if __name__ == '__main__':
    while True:
        fetch()
        time.sleep(60)
