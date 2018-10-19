#!/usr/bin/python
# coding:utf-8

import time
import ssl
import scrapy
from scrapy import Request
from scrapy.spiders import Rule, CrawlSpider

from common import configs
from msic.common import log
from worm.Items import MerchantItem, MerchantListItem
from msic.proxy.proxy_pool import proxy_pool
from scrapy.linkextractors import LinkExtractor

class QijiaSpider(CrawlSpider):
    ssl._create_default_https_context = ssl._create_unverified_context

    name = 'worm'
    allowed_domains = ['www.jia.com']
    start_urls = ['https://www.jia.com/zx/guangzhou/company/gexingbao']

    rules = (
        Rule(LinkExtractor(allow='/gexingbao/'), callback='parse_item', follow=True),
    )

    # def __init__(self, *args, **kwargs):
    #     urls = kwargs.pop('urls', [])  # 获取参数
    #     if urls:
    #         self.start_urls = urls.split(',')
    #         print('start urls = ', self.start_urls)

    def parse_item(self, response):
        """
        解析文章列表页,拿到页面上的链接，给内容解析页使用，如果有下一页，则调用本身 parse()
        """
        print('Begin parse ', response.url)

        list = response.xpath('//div[@class="company-item"]//div[@class="ordinary clearfix"]')

        for index, merchant in enumerate(list):
            if index != 0:
                break

            item = MerchantListItem()
            item['list_url'] = response.urljoin(
                merchant.xpath('./div[@class="list-middle fl"]/h2/a/@href').extract_first())
            item['category_name'] = merchant.xpath('./div[@class="list-middle fl"]/h2/a/text()').extract_first()
            item['merchant_id'] = merchant.xpath('./div[@class="list-right fl"]/a/@shop_id').extract_first()

            print('a href = ', item['list_url'])
            yield Request(url=item['list_url'], callback=self.parse_content)

        ## 是否还有下一页，如果有的话，则继续
        pages = response.xpath('//div[@class="p_page"]/a')
        cur_page_num = int(response.xpath('//div[@class="p_page"]/span[@class="cur"]/text()').extract_first())
        if pages:
            cur_index = 0
            next_index = 0
            for index, page_list in enumerate(pages):
                page_num_str = (page_list.xpath('./text()').extract_first())
                if self.is_number(page_num_str):
                    page_num = int(page_num_str)
                    if page_num > cur_page_num:
                        next_index = index
                        break

            if next_index < len(pages):
                next_page_url = response.urljoin(pages[next_index].xpath('./@href').extract_first())
                print('next_page_url: ', next_page_url)
                # 将 「下一页」的链接传递给自身，并重新分析
                yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_content(self, response):
        """
            解析文章内容
        """
        print('Begin parseContent ', response.url)

        item = MerchantItem()

        item['updated_at'] = int(time.time())
        item['url'] = response.url
        item['area'] = response.url.split('/')[4]
        item['merchant_id'] = response.url.split('/')[-2]

        try:
            item['merchant_name'] = response.xpath('//span[@id="shop_name_val"]/text()')[0].extract()
            item['company_profile'] = response.xpath('//div[@class="i-txt"]/span[@class="s-con"]/text()')[0].extract()

            item['service_area'] = \
                response.xpath('//div[@class="des"]/div[@class="item-des clearfix"]/div[@class="i-txt i-dTxt"]/text()')[
                    0].extract()

            item['merchant_pic'] = response.urljoin(response.xpath('//div[@class="pic"]/img/@src')[0].extract())
            yield item
        except Exception as e:
            print("-----------------------获取到json:" + response.text + "------------------------------")
            log.warn("%s ( refer: %s )" % (e, response.url))
            if configs.USE_PROXY:
                proxy_pool.add_failed_time(response.meta['proxy'].replace('http://', ''))

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False
