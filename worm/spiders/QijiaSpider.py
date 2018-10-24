#!/usr/bin/python
# coding:utf-8

import ssl
import time

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider
from common import configs
from msic.common import log
from msic.proxy.proxy_pool_ms import proxy_pool
from worm.Items import MerchantItem, MerchantListItem
from worm.service.CityStrategyService import CityStrategyService


class QijiaSpider(CrawlSpider):
    ssl._create_default_https_context = ssl._create_unverified_context

    name = 'worm'
    allowed_domains = ['www.jia.com']

    #    start_urls = ['https://www.jia.com/zx/guangzhou/company/gexingbao/',
    #                  'https://www.jia.com/zx/shanghai/company/gexingbao/',
    #                  'https://www.jia.com/zx/gdfs/company/gexingbao/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'worm.pipelines.MerchantSpiderPipeline': 302,
        }
    }

    # rules = (
    #    Rule(LinkExtractor(allow=r'/zx/[0-9]+?', restrict_css='div.company-item'), follow=True),  # 爬取下一页，默认follow
    #    Rule(LinkExtractor(allow=r'shop/[0-9]+/'), callback='parse_content', follow=False),
    # )

    def __init__(self, *args, **kwargs):
        self.city_service = CityStrategyService()
        city_list_do = self.city_service.find_all()
        self.city_list = []
        if city_list_do:
            for city in city_list_do:
                self.city_list.append('https://www.jia.com/zx/' + city.url.split('/')[-2] + '/company/gexingbao/')

        self.start_urls = self.city_list
        # urls = kwargs.pop('urls', [])  # 获取参数
        # if urls:
        #    self.start_urls = urls.split(',')
        #   log.info('start urls = ' + self.start_urls)

    def parse(self, response):
        """
        解析文章列表页,拿到页面上的链接，给内容解析页使用，如果有下一页，则调用本身 parse()
        """
        log.info('Begin parse ' + response.url)

        list = response.xpath('//div[@class="company-item"]//div[@class="ordinary clearfix"]')

        for index, merchant in enumerate(list):
            item = MerchantListItem()
            item['list_url'] = response.urljoin(
                merchant.xpath('./div[@class="list-middle fl"]/h2/a/@href').extract_first())
            item['category_name'] = merchant.xpath('./div[@class="list-middle fl"]/h2/a/text()').extract_first()
            item['merchant_id'] = merchant.xpath('./div[@class="list-right fl"]/a/@shop_id').extract_first()

            log.info('a href = ' + item['list_url'])
            yield Request(url=item['list_url'], callback=self.parse_content)

        ## 是否还有下一页，如果有的话，则继续
        pages = response.xpath('//div[@class="p_page"]/a')
        cur_page_xpath = response.xpath('//div[@class="p_page"]/span[@class="cur"]/text()')
        if cur_page_xpath is None:
            cur_page_num = 1
        else:
            cur_page_num = int(cur_page_xpath.extract_first())
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
                log.info('next_page_url: ' + next_page_url)
                # 将 「下一页」的链接传递给自身，并重新分析
                yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_content(self, response):
        """
            解析文章内容
        """
        log.info(('Begin parseContent ' + response.url))

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
            # log.warn("-----------------------获取到内容:" + response.text + "------------------------------")
            log.warn("spider error %s ( refer: %s )" % (e, response.url))
            log.error(e)
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
