from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TEXT, INTEGER

from worm.Connections import Base


class MerchantDO(Base):
    # 表的名字:
    __tablename__ = 'merchant'

    # 表的结构:
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # ID
    updated_at = Column(INTEGER)  # 最后一次更新时间

    merchant_pic = Column(TEXT)  # 图标
    merchant_name = Column(TEXT)  # 名称
    service_area = Column(TEXT)
    company_profile = Column(TEXT)
    merchant_id = Column(TEXT)
    url = Column(TEXT)
    area = Column(TEXT)

# class MerchantListDO(Base):
#     # 表的名字:
#     __tablename__ = 'merchant_list'
#
#     # 表的结构:
#     id = Column(INTEGER, primary_key=True, autoincrement=True)  # ID
#     updated_at = Column(INTEGER)  # 最后一次更新时间
#
#     url = Column(TEXT)
#     item_name = Column(TEXT)
#     merchant_id = Column(TEXT)
#     area = Column(TEXT)
