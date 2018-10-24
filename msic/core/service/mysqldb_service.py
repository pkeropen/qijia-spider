# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from common.connections import db_session
from msic.common import utils
from model.Models import ProxyDO
# sqlalchemy model 基类
from msic.proxy.proxy import Proxy

Base = declarative_base()


class MysqlDbService(object):
    def __init__(self):
        self.session = db_session()

    def convert(self, item: Proxy):
        if isinstance(item, Proxy):
            model = ProxyDO()
            model.ip = item.ip
            model.origin = item.origin
            model.create_time = item.create_time
            model.update_time = item.update_time
            model.failed_count = item.failed_count
            model.response_speed = item.response_speed
            model.validity = (1 if item.validity is True else 0)
            return model
        return None

    def insert_one(self, item: ProxyDO):
        if isinstance(item, ProxyDO):
            session = self.session()

            try:
                m = session.query(ProxyDO).filter(ProxyDO.ip == item.ip).first()
                if m is None:  # 插入数据
                    session.add(item)
                    session.flush()
                else:
                    m.origin = item.origin
                    m.update_time = item.update_time
                    m.failed_count = item.failed_count
                    m.response_speed = item.response_speed
                    m.validity = item.validity

                session.commit()

            except Exception as error:
                session.rollback()
                utils.log(error)
                raise
            finally:
                session.close()

    def find_all(self):
        session = self.session()

        try:
            m = session.query(ProxyDO).order_by(ProxyDO.failed_count.asc(), ProxyDO.validity.desc(),
                                                ProxyDO.response_speed.asc(), ProxyDO.update_time.desc()).all()
            return m
        except Exception as error:
            session.rollback()
            utils.log(error)
            raise
        finally:
            session.close()

    def find_one(self, ip: str):
        session = self.session()

        try:
            m = session.query(ProxyDO).filter(ProxyDO.ip == ip).first()
            return m
        except Exception as error:
            session.rollback()
            utils.log(error)
            raise
        finally:
            session.close()

    def count(self):
        session = self.session()
        try:
            count = session.query(ProxyDO).count()
            return count
        except Exception as error:
            utils.log(error)
            raise
        finally:
            session.close()

    def detele_all(self):
        session = self.session()
        try:
            session.query(ProxyDO).delete()
            session.commit()
        except Exception as error:
            session.rollback()
            utils.log(error)
            raise
        finally:
            session.close()

    def detele_one(self, ip):
        session = self.session()
        try:
            session.query(ProxyDO).filter(ProxyDO.ip == ip).delete()
            session.commit()
        except Exception as error:
            session.rollback()
            utils.log(error)
            raise
        finally:
            session.close()
