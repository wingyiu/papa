# -*- coding: utf-8 -*-
import os
import sys
import re
from urllib.parse import urljoin
import redis

CUR_DIR = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(CUR_DIR, ".."))  # !

import torndb_pymysql as torndb
from crawl.settings import MYSQLS, REDISS
from crawl.settings import REDIS_START_URLS_KEY
from crawl.spiders.soufun_loupan_fangjia import SFLPFangjiaSpider


def import_start_urls():
    db = torndb.Connection(host='%s:%s' % (MYSQLS['default']['HOST'], MYSQLS['default']['PORT']),
                           database=MYSQLS['default']['NAME'],
                           user=MYSQLS['default']['USER'],
                           password=MYSQLS['default']['PASSWORD'],
                           )
    client = redis.StrictRedis(host=REDISS['default']['host'],
                               port=REDISS['default']['port'],
                               db=REDISS['default']['db'])

    key = REDIS_START_URLS_KEY % {'name': SFLPFangjiaSpider.name}
    page = 0
    page_size = 50
    while True:
        offset = page * page_size
        count = page_size
        lps = db.query('SELECT id, rid, name, price_url FROM lp_links_copy_httpuncomplete LIMIT %s, %s', offset, count)

        # 拼接url,存入redis
        for lp in lps:
            lk = lp['price_url'].strip()
            if not lk:
                # http://esf.jx.fang.com/house-xm2014988160/
                if 'http://esf.' in lk:
                    r = r'^http://esf\.\w*\.?fang\.com/(house|shop)-xm(\d+)/$'
                    p = re.compile(r)
                    ms = p.findall(lp['link'])
                    rid = ms[0][1]
                    url = 'http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&KeyWord=%s&year=2' % (rid, )
                    print('%s %s' % (lp['id'], url))
                    client.sadd(key, url)
            else:
                if lk.endswith('/jiage/'):
                    if lp['rid']:
                        url = 'http://fangjia.fang.com/pinggu/ajax/ChartAjaxContainMax.aspx?dataType=proj&KeyWord=%s&year=2' % (lp['rid'])
                        print('%s %s' % (lp['id'], url))
                        client.sadd(key, url)
                    else:
                        print('%s %s' % (lp['id'], lk))
                        client.sadd(key, lk)
                elif lk.endswith('/fangjia.htm'):
                    print('%s %s' % (lp['rid'], lk))
                    client.sadd(key, lk)
                else:  # 修正urlhttp://hengxinhuayuandqu.fang.com/house/2821108970gjia.htm
                    r = r'^http://\w*\.fang\.com/[a-zA-z0-9/]*?/(\d+)gjia\.htm$'
                    p = re.compile(r)
                    ms = p.findall(lp['price_url'])
                    rid = ms[0]
                    url = lp['price_url'].replace(rid, rid + '/fan')
                    print('%s %s' % (rid, url))
                    client.sadd(key, url)

        if len(lps) < page_size:
            break

        page += 1


if __name__ == '__main__':
    import_start_urls()

