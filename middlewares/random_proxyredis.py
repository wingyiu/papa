# Copyright (C) 2013 by Aivars Kalvans <aivars.kalvans@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re
import random
import base64
import logging
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
import redis
import time

log = logging.getLogger('scrapy.proxies')


class RandomProxyMiddleware(object):

    def __init__(self, settings):
        self.host = settings.get('REDISS')['default']['host']
        self.port = settings.get('REDISS')['default']['port']
        self.db = settings.get('REDISS')['default']['db']
        self.alive_key = settings.get('REDIS_PROXY_ALIVE_KEY')
        self.pool_key = settings.get('REDIS_PROXY_POOL_KEY')
        self.client = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings)
        return o

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False

        while True:
            proxies_cnt = self.client.scard(self.alive_key)
            if not proxies_cnt:
                log.warning('All proxies are unusable, cannot proceed')
                time.sleep(5)
            else:
                proxy_ip_raw = self.client.srandmember(self.alive_key)
                if not proxy_ip_raw:
                    time.sleep(5)
                else:
                    proxy_address = proxy_ip_raw.decode('utf-8').strip()
                    request.meta['proxy'] = proxy_address
                    log.debug('Using proxy <%s>, %d proxies left' % (proxy_address, proxies_cnt))
                    return

    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return

        proxy = request.meta['proxy']
        request.meta["exception"] = True

        log.warning('Failed proxy: <%s>' % (proxy,))

        log.info('move proxy <%s> from alive to pool' % (proxy,))
        self.client.smove(self.alive_key, self.pool_key, proxy)
