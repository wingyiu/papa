# -*- coding: utf-8 -*-
import re
import scrapy
import json
from proxy.items import ProxyItem


class XiciDailiSpider(scrapy.Spider):
    """西刺免费代理IP"""
    name = "proxy_xicidaili"
    start_urls = [
        'http://www.xicidaili.com/wt/1',
        'http://www.xicidaili.com/wn/1',
        'http://www.xicidaili.com/nn/1',
        'http://www.xicidaili.com/nt/1',
    ]

    def parse(self, response):
        rows = response.css('table#ip_list tr')
        for i, row in enumerate(rows):
            if i == 0:
                continue
            cols = row.css('td')
            r = {
                'ip': cols[1].css('::text').extract_first().strip(),
                'port': cols[2].css('::text').extract_first().strip(),
                'scheme': cols[5].css('::text').extract_first().strip().lower(),
                'anno': cols[4].css('::text').extract_first().strip(),
            }
            if r['anno'] == '高匿' and r['scheme'] in ['http', 'https']:
                yield ProxyItem(**r)

        next_pages = response.css('div.pagination a::attr("href")').extract()
        for np in next_pages:
            p = np.split('/')[-1]
            if not int(p) > 5:
                yield response.follow(np, self.parse)


class KuaidailiVIPSpider(scrapy.Spider):
    name = 'proxy_kuaidaili'
    # http://www.kuaidaili.com/genapiurl/?orderid=978956339172676
    start_urls = ['http://svip.kuaidaili.com/api/getproxy/?orderid=978956339172676&num=5000&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_ha=1&sep=2']

    def parse(self, response):
        lines = response.text.split('\n')
        for line in lines:
            ip, port = line.split(':')
            yield ProxyItem(ip=ip, port=port, scheme='http', anno='高匿')


# class GoubanjiaSpider(scrapy.Spider):
#     """goubanjia代理IP 不可用 难搞"""
#     name = "proxy_goubanjia"
#     start_urls = [
#         'http://www.goubanjia.com/free/gngn/index1.shtml',
#         'http://www.goubanjia.com/free/gwgn/index1.shtml',
#     ]
#
#     def parse(self, response):
#         rows = response.css('#list table tbody tr')
#         for i, row in enumerate(rows):
#             if i == 0:
#                 continue
#             cols = row.css('td')
#             r = {
#                 'ip': cols[0].xpath('.//text()').strip(),
#                 'port': cols[2].css('::text').extract_first().strip(),
#                 'scheme': cols[5].css('::text').extract_first().strip().lower(),
#                 'anno': cols[4].css('::text').extract_first().strip(),
#             }
#             if r['anno'] == '高匿' and r['scheme'] == 'http':
#                 yield ProxyItem(**r)
#
#         next_pages = response.css('div.pagination a::attr("href")').extract()
#         for np in next_pages:
#             p = np.split('/')[-1]
#             if not int(p) > 5:
#                 yield response.follow(np, self.parse)


class LiuliuIPCNaSpider(scrapy.Spider):
    """66ip.cn"""
    name = "proxy_66ipcn"
    start_urls = [
        'http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=4&start=&ports=&export=&ipaddress=&area=0&proxytype=2&api=66ip',
    ]

    def parse(self, response):
        p = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}'
        proxies = re.findall(p, response.text)
        for proxy in proxies:
            h, p = proxy.split(':')
            r = {'ip': h, 'port': p, 'scheme': 'http', 'anno': '高匿'}
            yield ProxyItem(**r)


class IP181Spider(scrapy.Spider):
    """www.ip181.com"""
    name = "proxy_ip181"
    start_urls = [
        'http://www.ip181.com/',
    ]

    def parse(self, response):
        rows = response.css('table tbody tr')
        for i, row in enumerate(rows):
            if i == 0:
                continue
            cols = row.css('td')
            r = {
                'ip': cols[0].css('::text').extract_first().strip(),
                'port': cols[1].css('::text').extract_first().strip(),
                'scheme': cols[3].css('::text').extract_first().strip().lower(),
                'anno': cols[2].css('::text').extract_first().strip(),
            }
            if r['anno'] != '透明' and r['scheme'] in ['http', 'https']:
                yield ProxyItem(**r)


class Data5uSpider(scrapy.Spider):
    """www.data5u.com"""
    name = "proxy_data5u"
    start_urls = [
        'http://www.data5u.com/free/gngn/index.shtml',
        'http://www.data5u.com/free/gwgn/index.shtml',
    ]

    def parse(self, response):
        rows = response.css('.wlist .l2')
        for i, row in enumerate(rows):
            if i == 0:
                continue
            cols = row.css('li')
            r = {
                'ip': cols[0].css('::text').extract_first().strip(),
                'port': cols[1].css('::text').extract_first().strip(),
                'scheme': cols[3].css('a::text').extract_first(),
                'anno': cols[2].css('a::text').extract_first(),
            }
            if '匿' in r['anno'] and r['scheme'] in ['http', 'https']:
                yield ProxyItem(**r)


# class MimvpSpider(scrapy.Spider):
#     """http://proxy.mimvp.com/free.php [x]"""
#     name = "proxy_mimvp"
#     start_urls = [
#         'http://proxy.mimvp.com/free.php?proxy=in_hp&sort=&page=1',
#     ]
#
#     def parse(self, response):
#         # print(response.text)
#         ips = response.css('table.free-table tbody .tbl-proxy-id::text').extract()
#         ports = response.css('table.free-table tbody .tbl-proxy-port img::attr(src)').extract()
#         types = response.css('table.free-table tbody .tbl-proxy-type::text').extract()
#         anons = response.css('table.free-table tbody .tbl-proxy-anonymous::text').extract()
#
#         for i, row in enumerate(ips):
#             r = {
#                 'ip': ips[i],
#                 'port': ports[i],
#                 'scheme': types[i],
#                 'anno': anons[i],
#             }
#             print(r)
#             # yield ProxyItem(**r)


class KxdailiSpider(scrapy.Spider):
    """开心代理"""
    name = "proxy_kxdaili"
    start_urls = [
        'http://www.kxdaili.com/dailiip/1/1.html#ip',
    ]

    def parse(self, response):
        rows = response.css('table.ui tbody tr')
        for i, row in enumerate(rows):
            if i == 0:
                continue
            cols = row.css('td')
            r = {
                'ip': cols[0].css('::text').extract_first().strip(),
                'port': cols[1].css('::text').extract_first().strip(),
                'scheme': cols[3].css('::text').extract_first().strip().lower(),
                'anno': cols[2].css('::text').extract_first().strip(),
            }
            if r['anno'] == '高匿' and r['scheme'] in ['http', 'https']:
                yield ProxyItem(**r)

        next_pages = response.css('div.page a::attr("href")').extract()
        for np in next_pages:
            yield response.follow(np, self.parse)


class YaoyaodailiSpider(scrapy.Spider):
    name = "proxy_yaoyaodaili"
    start_urls = [
        'http://www.httpsdaili.com/?stype=1&page=1',
        'http://www.httpsdaili.com/?stype=3&page=1',
    ]

    def parse(self, response):
        rows = response.css('#list table tbody tr')
        for i, row in enumerate(rows):
            cols = row.css('td')
            r = {
                'ip': cols[0].css('::text').extract_first().strip(),
                'port': cols[1].css('::text').extract_first().strip(),
                'scheme': cols[3].css('::text').extract_first().strip().lower(),
                'anno': '高匿',
            }
            if r['anno'] == '高匿' and r['scheme'] in ['http', 'https']:
                yield ProxyItem(**r)

        next_pages = response.css('#listnav ul a::attr("href")').extract()
        for np in next_pages:
            yield response.follow(np, self.parse)
