# -*- coding: utf-8 -*-
from common.connections import db_session
from msic.common import log
from worm.Items import MerchantItem
from model.Models import MerchantDO


class MerchantStrategyService(object):

    def __init__(self):
        self.session = db_session()

    def handle_item(self, item: MerchantItem):
        log.info('process item from worm url = ' + item['url'])

        if isinstance(item, MerchantItem):

            session = self.session()

            model = MerchantDO()
            model.updated_at = item['updated_at']
            model.merchant_name = item['merchant_name']
            model.company_profile = item['company_profile']
            model.service_area = item['service_area']
            model.merchant_pic = item['merchant_pic']
            model.merchant_id = item['merchant_id']
            model.url = item['url']
            model.area = item['area']

            try:
                m = session.query(MerchantDO).filter(MerchantDO.url == model.url).first()

                if m is None:  # 插入数据
                    log.info('add model from worm url = ' + model.url)
                    session.add(model)
                    session.flush()
                    session.commit()
                    log.info('spider_success url = ' + model.url)

                # else:  # 更新数据
                #    log.info("update model from gp url " + model.url)
                #    m.updated_at = item['updated_at']
                #    m.merchant_name = item['merchant_name']
                #    m.merchant_pic = item['merchant_pic']
                #    m.service_area = item['service_area']
                #    m.merchant_id = item['merchant_id']
                #    m.company_profile = item['company_profile']
            #     m.area = item['area']
            #    m.url = item['url']

            except Exception as error:
                session.rollback()
                log.error(error)
                raise
            finally:
                session.close()
        return item

