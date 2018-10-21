# -*- coding: utf-8 -*-

import scrapy


# 店铺
class MerchantItem(scrapy.Item):
    updated_at = scrapy.Field()  # 最后一次更新时间
    merchant_name = scrapy.Field()  # 名称
    merchant_pic = scrapy.Field()  # 图片
    service_area = scrapy.Field()  # 服务区域
    company_profile = scrapy.Field()  # 公司简介
    url = scrapy.Field()
    merchant_id = scrapy.Field()
    area = scrapy.Field()  # 地区


# 店铺列表
class MerchantListItem(scrapy.Item):
    list_url = scrapy.Field()  # 链接
    page_num = scrapy.Field()  # 当前页
    category_name = scrapy.Field()  # 分类
    merchant_id = scrapy.Field()


# 城市
class CityItem(scrapy.Item):
    url = scrapy.Field()  # 链接
    name = scrapy.Field()  # 名称
    create_at = scrapy.Field()