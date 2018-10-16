#!/usr/bin/python
# coding:utf-8

import time

import scrapy

from dianping.Items import MerchantItem, MerchantListItem


class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['play.google.com']

    def __init__(self, *args, **kwargs):
        urls = kwargs.pop('urls', [])  # 获取参数
        if urls:
            self.start_urls = urls.split(',')
            print('start urls = ', self.start_urls)

    """
         解析文章列表页
    """

    def parse(self, response):
        print('Begin parse ', response.url)

        item = MerchantListItem()
        content = response.xpath('//div[@class="LXrl4c"]')

        exception_count = 0

        try:
            item['merchant_name'] = content.xpath('//h1[@class="AHFaub"]/span/text()')[0].extract()
        except Exception as error:
            exception_count += 1
            print('merchant_name except = ', error)
            item['merchant_name'] = ''

        if exception_count >= 3:
            print('spider_failure_parse_too_much_exception')
            return

        yield item

    """
        解析文章内容页
    """

    def parseContent(self, response):
        print('Begin parse ', response.url)

        item = MerchantItem()
        item['updated_at'] = int(time.time())

        # try:
        #     item['merchant_name'] = content.xpath('//h1[@class="AHFaub"]/span/text()')[0].extract()
        # except Exception as error:
        #     exception_count += 1
        #     print('merchant_name except = ', error)
        #     item['merchant_name'] = ''


