# -*- coding: utf-8 -*-

import scrapy


# 店铺
class MerchantItem(scrapy.Item):
    merchant_name = scrapy.Field()  # 名称
    updated_at = scrapy.Field()  # 最后一次更新时间


# 店铺列表
class MerchantListItem(scrapy.Item):
    list_url = scrapy.Field()  # 链接
    page_num = scrapy.Field()  # 当前页
    category_name = scrapy.Field()  # 分类
