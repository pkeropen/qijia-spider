#!/usr/bin/python
# coding:utf-8

import time
import ssl
import scrapy
from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider

from common import configs
from msic.common import log
from worm.Items import MerchantItem, MerchantListItem, CityItem
from msic.proxy.proxy_pool_ms import proxy_pool
from scrapy.linkextractors import LinkExtractor


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
