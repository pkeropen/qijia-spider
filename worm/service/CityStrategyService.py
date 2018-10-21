# -*- coding: utf-8 -*-
from common.connections import db_session
from msic.common import log
from worm.Items import CityItem
from model.Models import CityDO


class CityStrategyService(object):

    def __init__(self):
        self.session = db_session()

    def handle_item(self, item: CityItem):
        log.info('process item from worm url = ' + item['url'])

        if isinstance(item, CityItem):

            session = self.session()

            model = CityDO()
            model.name = item['name']
            model.url = item['url']
            model.create_at = item['create_at']

            try:
                m = session.query(CityDO).filter(CityDO.url == model.url).first()

                if m is None:  # 插入数据
                    log.info('add model from worm url = ' + model.url)
                    session.add(model)
                    session.flush()
                    session.commit()
                    log.info('spider_success url = ' + model.url)


            except Exception as error:
                session.rollback()
                log.error(error)
                raise
            finally:
                session.close()
        return item

    def find_all(self):
        session = self.session()

        try:
            city_list = session.query(CityDO).all()
            return city_list
        except Exception as e:
            log.error(e)
        finally:
            session.close()
