# papa
爬爬


````

source /root/venv/crawl/bin/activate
pip3 install -r requirements.txt

nohup python bin/kuaidaili.py >> kuaidiali.out &
nohup sh bin/get_proxies.sh >> getproxies.out &

nohup scrapy crawl soufun_lp_fangjia >> crawl_fj_01.out 2>&1 &

tail -f crawl_fj_01.out
````
