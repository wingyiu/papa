# -*- coding: utf-8 -*-
"""
维护代理IP池，找出还可用的IP
"""
import sys
import os
import time
import requests
import redis
import random
from multiprocessing.dummy import Pool

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))  #

test_urls = ['http://sz.fang.com', 'http://gz.fang.com', 'http://bj.fang.com', 'http://sh.fang.com']
test_str = '房'
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'}
TIMEOUT = 20
TEST_WORKER_SIZE = 64
ENCODING = 'gbk'

from proxy.settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PROXY_POOL_KEY, REDIS_PROXY_BAD_KEY, REDIS_PROXY_ALIVE_KEY, REDIS_PROXY_DEAD_KEY


def filter():
    """对pool里的ip进行检测，好的扔alive，坏的扔bad里"""
    client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    with Pool(TEST_WORKER_SIZE) as pool:
        while client.scard(REDIS_PROXY_POOL_KEY):
            proxies = []
            for i in range(TEST_WORKER_SIZE):
                p = client.spop(REDIS_PROXY_POOL_KEY)
                if p:
                    proxies.append(p)

            if len(proxies) < TEST_WORKER_SIZE:
                break

            test_results = pool.map(test, proxies)
            for i, res in enumerate(test_results):
                if res:
                    client.sadd(REDIS_PROXY_ALIVE_KEY, proxies[i])
                else:
                    client.sadd(REDIS_PROXY_BAD_KEY, proxies[i])


def test(proxy):
    line = proxy.decode('utf-8').strip()
    sch = line.split(':')[0]
    if sch != 'http' and sch != 'https':
        print('%s [SKIP]' % (line,))
        return False
    proxies = {'http': line, 'https': line}
    url = random.choice(test_urls)
    try:
        st = time.time()
        r = requests.get(url, headers=headers, proxies=proxies, timeout=TIMEOUT)
        cost = time.time() - st
        # 单从status code判断是不靠谱的，代理自己可能会从定向
        # 比如出现有些代理调到一个内网上网认证页面 http://172.23.3.10:90/ac_portal/proxy.html?template=default&tabs=pwd&vlanid=0
        # 所以要判断页面内容
        rtext = r.content.decode(ENCODING)
        # test_str = line.split('/')[-1].split(':')[0]
        if str(r.status_code) == '200' and test_str in rtext:
            print('%s %s %.2f [√]' % (line, r.status_code, cost))
            return True
        else:
            print('%s %s %.2f [×]' % (line, r.status_code, cost))
            return False
    except Exception as e:
        print('%s [×]' % (line, ))
        print(e)
        return False


def recycle():
    """从bad里面进行垃圾回收，可以用的扔回alive"""
    client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    with Pool(TEST_WORKER_SIZE) as pool:
        while client.scard(REDIS_PROXY_BAD_KEY):
            proxies = []
            for i in range(TEST_WORKER_SIZE):
                p = client.spop(REDIS_PROXY_BAD_KEY)
                if p:
                    proxies.append(p)

            if len(proxies) < TEST_WORKER_SIZE:
                break

            test_results = pool.map(test, proxies)
            for i, res in enumerate(test_results):
                if res:
                    client.sadd(REDIS_PROXY_ALIVE_KEY, proxies[i])
                else:
                    client.sadd(REDIS_PROXY_DEAD_KEY, proxies[i])


if __name__ == '__main__':
    while True:
        filter()
        time.sleep(5)
