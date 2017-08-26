# -*- coding: utf-8 -*-
import re
import datetime
import json
from urllib.parse import urlparse, parse_qs

import scrapy
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider
from scrapy.exceptions import CloseSpider
from crawl.items import PriceEntryItem


class SFLPFangjiaSpider(RedisSpider):
    """房价走势"""
    name = "soufun_lp_fangjia"
    start_urls = [
        # 'http://sijiyangguangzj0755.fang.com/house/2811100216/fangjia.htm',
        # 'http://wankelushan.fang.com/house/2810135142/fangjia.htm',
        # 'http://xinchangxiaoqu0379.fang.com/jiage/',
        # 'http://mingshihuayuan0574.fang.com/jiage/',
        # 'http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&KeyWord=2212040486&year=2',
        'http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&KeyWord=2212277806&year=2',
    ]
    proxy_usedout = False

    def parse(self, response):
        if self.proxy_usedout:
            raise CloseSpider(reason='代理用光了')

        self.logger.info(response.url)
        # http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&KeyWord=%s&year=2
        if response.url.startswith('http://fangjia.fang.com'):

            if not response.text:
                return

            self.logger.info('以API方式解析')
            # 提取楼盘id
            o = urlparse(response.url)
            qs = parse_qs(o.query)
            lp_id = qs['KeyWord'][0]

            try:
                prices_str = response.text.split('&')[0]
                prices = json.loads(prices_str)
                for p in prices:
                    r = {
                        'date': datetime.datetime.fromtimestamp(int(p[0])/1000).strftime('%Y-%m-%d'),
                        'avg_price': p[1],
                        'description': '',
                        'lp_id': lp_id,
                    }
                    yield PriceEntryItem(**r)
                self.logger.info('以API方式解析成功')
                return
            except:
                self.logger.exception('以API方式解析失败')

        else:
            # http://sijiyangguangzj0755.fang.com/house/2811100216/fangjia.htm
            try:
                self.logger.info('以新房房价趋势页方式解析')
                r = r'^http://\w*\.fang\.com/[a-zA-z0-9/]*?/(\d+)/fangjia\.htm$'
                p = re.compile(r)
                ms = p.findall(response.url)
                rid = ms[0]
                rows = response.css('#priceListOpen table tr')
                for i, row in enumerate(rows):
                    if i == 0:
                        continue
                    cols = row.css('td')
                    r = {
                        'date': cols[0].xpath('.//text()').extract_first().strip(),
                        'avg_price': cols[2].css('::text').extract_first().strip(),
                        'min_price': cols[1].css('::text').extract_first().strip(),
                        'max_price': cols[3].css('::text').extract_first().strip(),
                        'description': cols[4].css('::text').extract_first().strip(),
                        'lp_id': rid,
                    }
                    r['avg_price'] = r['avg_price'].replace('元/平方米', '')
                    r['min_price'] = r['min_price'].replace('元/平方米', '')
                    r['max_price'] = r['max_price'].replace('元/平方米', '')
                    if r['avg_price'] or r['min_price'] or r['max_price']:
                        yield PriceEntryItem(**r)
                self.logger.info('以新房房价趋势页方式解析成功')
                return
            except:
                self.logger.exception('以新房房价趋势页方式解析失败')
                pass

            # http://shop.sh.fang.com/house/1210671270/fangjia.htm
            try:
                self.logger.info('以商铺房价趋势页方式解析')
                r = r'^http://\w*\.fang\.com/[a-zA-z0-9/]*?/(\d+)/fangjia\.htm$'
                p = re.compile(r)
                ms = p.findall(response.url)
                rid = ms[0]
                rows = response.css('#salePriceListOpen table tr')
                for i, row in enumerate(rows):
                    if i == 0:
                        continue
                    cols = row.css('td')
                    r = {
                        'date': cols[0].xpath('.//text()').extract_first().strip(),
                        'avg_price': cols[2].css('::text').extract_first().strip(),
                        'min_price': cols[1].css('::text').extract_first().strip(),
                        'max_price': cols[3].css('::text').extract_first().strip(),
                        'description': cols[4].css('::text').extract_first().strip(),
                        'lp_id': rid,
                    }
                    r['avg_price'] = r['avg_price'].replace('元/平方米', '')
                    r['min_price'] = r['min_price'].replace('元/平方米', '')
                    r['max_price'] = r['max_price'].replace('元/平方米', '')
                    if r['avg_price'] or r['min_price'] or r['max_price']:
                        yield PriceEntryItem(**r)
                self.logger.info('以商铺房价趋势页方式解析成功')
                return
            except:
                self.logger.exception('以商铺房价趋势页方式解析失败')
                pass

            # http://office.zz.fang.com/house/2510147567/fangjia.htm
            try:
                self.logger.info('以办公室租价趋势页方式解析')
                r = r'^http://\w*\.fang\.com/[a-zA-z0-9/]*?/(\d+)/fangjia\.htm$'
                p = re.compile(r)
                ms = p.findall(response.url)
                rid = ms[0]
                rows = response.css('#rentPriceListOpen table tr')
                for i, row in enumerate(rows):
                    if i == 0:
                        continue
                    cols = row.css('td')
                    r = {
                        'date': cols[0].xpath('.//text()').extract_first().strip(),
                        'avg_price': cols[2].css('::text').extract_first().strip(),
                        'min_price': cols[1].css('::text').extract_first().strip(),
                        'max_price': cols[3].css('::text').extract_first().strip(),
                        'description': cols[4].css('::text').extract_first().strip(),
                        'lp_id': rid,
                    }
                    r['avg_price'] = r['avg_price'].replace('元/平方米', '')
                    r['min_price'] = r['min_price'].replace('元/平方米', '')
                    r['max_price'] = r['max_price'].replace('元/平方米', '')
                    if r['avg_price'] or r['min_price'] or r['max_price']:
                        yield PriceEntryItem(**r)
                self.logger.info('以办公室租价趋势页方式解析成功')
                return
            except:
                self.logger.exception('以办公室租价趋势页方式解析失败')
                pass

            try:
                self.logger.info('以二手房房价趋势解析')
                xx = response.css('.trendIframe1 iframe::attr(src)').extract_first().strip()
                o = urlparse(xx)
                qs = parse_qs(o.query)
                lp_id = qs['newcode'][0]
                url = 'http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&KeyWord=%s&year=2' % (lp_id, )
                self.logger.info(url)
                req = scrapy.Request(url=url, callback=self.parse)
                yield req
                self.logger.info('以二手房房价趋势解析成功')
            except:
                # 有没有房价的情况 http://office.qd.fang.com/house/2411728681/fangjia.htm
                self.logger.exception('以二手房房价趋势解析失败')
                self.logger.debug(response.url)





