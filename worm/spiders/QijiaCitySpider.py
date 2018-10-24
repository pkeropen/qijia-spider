#!/usr/bin/python
# coding:utf-8

import ssl
import time

from scrapy.spiders import CrawlSpider

from msic.common import log
from worm.Items import CityItem


class QijiaCitySpider(CrawlSpider):
    ssl._create_default_https_context = ssl._create_unverified_context

    name = 'worm'
    allowed_domains = ['www.jia.com']
    start_urls = ['https://www.jia.com/citylist/']


    # def __init__(self, *args, **kwargs):
    # urls = kwargs.pop('urls', [])  # 获取参数
    # if urls:
    #     self.start_urls = urls.split(',')
    #     log.info('start urls = ' + self.start_urls)

    custom_settings = {
        'ITEM_PIPELINES': {
            'worm.pipelines.CitySpiderPipeline': 302,
        }
    }

    def parse(self, response):
        """
        解析内容
        """
        log.info('Begin parse ' + response.url)

        list = response.xpath('//div[@class="city_main"]/dl[@class="clearfix"]/dd/a')

        for index, city in enumerate(list):
            item = CityItem()
            item['url'] = response.urljoin(
                city.xpath('./@href').extract_first())
            item['name'] = city.xpath('./text()').extract_first()
            item['create_at'] = int(time.time())
            log.info('a href = ' + item['url'])
            yield item

        log.info('End parse ' + response.url)
