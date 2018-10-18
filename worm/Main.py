from scrapy import cmdline

cmdline.execute(r"scrapy crawl worm -a urls=https://www.jia.com/zx/guangzhou/company/gexingbao/?order=koubei&page=2".split())
