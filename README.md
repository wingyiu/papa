# papa
爬爬


nohup python bin/kuaidaili.sh >> kuaidiali.out &
nohup sh bin/get_proxies.sh >> getproxies.out &

nohup scrapy crawl soufun_lp_fangjia >> crawl_fj_01.out 2>&1 &

tail -f crawl_fj_01.out
