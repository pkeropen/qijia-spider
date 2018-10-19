from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TEXT, INTEGER

from common.connections import Base


class ProxyDO(Base):
    # 表的名字:
    __tablename__ = 'proxy_list'

    # 表的结构:
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # ID

    ip = Column(TEXT)
    origin = Column(TEXT)
    create_time = Column(TEXT)
    update_time = Column(TEXT)
    failed_count = Column(INTEGER)
    response_speed = Column(INTEGER)
    validity = Column(INTEGER)

