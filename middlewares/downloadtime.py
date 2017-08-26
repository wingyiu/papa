# -*- coding: utf-8 -*-
"""
log the download cost time
"""
import logging
import time

from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed

from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from scrapy.core.downloader.handlers.http11 import TunnelError


logger = logging.getLogger(__name__)


class DownloadTimeLoggingMiddleware(object):

    def __init__(self, settings):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta['start_time'] = time.time()

    def process_response(self, request, response, spider):
        s_t = request.meta.get('start_time', None)
        end_t = time.time()
        cost = end_t - s_t
        logger.info('%s downloaded, cost time: %.2fS', request.url, cost)

        return response

    def process_exception(self, request, exception, spider):
        s_t = request.meta.get('start_time', None)
        end_t = time.time()
        cost = end_t - s_t
        logger.info('%s raise exception, cost time: %.2fS', request.url, cost)

