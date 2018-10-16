#!/usr/bin/python
# coding:utf-8

import time
from urllib import parse
import ssl
import scrapy
from scrapy import Request

from dianping.Items import MerchantItem, MerchantListItem

ssl._create_default_https_context = ssl._create_unverified_context

class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['www.dianping.com']

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
        content = response.xpath('//div[@class="shop-title"]/h3/a/text()')
        exception_count = 0

        for title in content:
            post_url = title.css("::attr(href)").extract_first()
            yield Request(url=post_url,callback=self.parseContent)

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
