from scrapy import cmdline

cmdline.execute(r"scrapy crawl dianping -a urls=http://www.dianping.com/foshan/ch90/".split())
