# -*- coding: utf-8 -*-
from worm.service.MerchantStrategyService import MerchantStrategyService


class MerchantSpiderPipeline(object):
    def __init__(self):
        self.merchant_strategy_service = MerchantStrategyService()

    def process_item(self, item, spider):
        self.merchant_strategy_service.handle_item(item)
