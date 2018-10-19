import os
import sys
import threading
import time
from os.path import dirname

from schedule import Scheduler
from twisted.internet import reactor

from common import configs

# path = dirname(os.path.abspath(os.path.dirname(__file__)))
# sys.path.append(path)

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals, cmdline
from pydispatch import dispatcher
from worm.spiders.QijiaSpider import QijiaSpider
from msic.proxy.proxy_pool_ms import proxy_pool


# cmdline.execute(r"scrapy crawl worm -a urls=https://www.jia.com/zx/guangzhou/company/gexingbao/?order=koubei&page=2".split())

class Runner(object):

    def __init__(self):
        self.is_running = False
        dispatcher.connect(self.pause_crawler, signals.engine_stopped)
        self.setting = get_project_settings()
        self.process = None

    def start_scrapy(self):
        self.process = CrawlerProcess(self.setting)
        self.crawl()
        reactor.run()

    def pause_crawler(self):
        self.is_running = False
        print("============ 爬虫已停止 ===================")

    def crawl(self):
        self.is_running = True
        self.process.crawl(QijiaSpider())

    def start_proxy_pool(self):
        if configs.USE_PROXY:
            proxy_pool.start()
        else:
            proxy_pool.drop_proxy()

    def run(self):
        self.start_proxy_pool()
        self.start_scrapy()


if __name__ == '__main__':
    runner = Runner()


    def thread_task():
        def task():
            if not runner.is_running:
                print("============ 开始重新爬取 ===================")
                runner.crawl()

        schedule = Scheduler()
        schedule.every(30).minutes.do(task)

        while True:
            schedule.run_pending()
            time.sleep(1)


    thread = threading.Thread(target=thread_task)
    thread.start()

    runner.run()
