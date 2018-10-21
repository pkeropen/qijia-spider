#!/usr/bin/python
# coding:utf-8
import os
import platform
import redis
from msic.core.service import mongodb_service

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if platform.system() == "Windows":
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/win/chromedriver.exe")
else:
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/mac64/chromedriver")

# 浏览器路径
CHROME_DRIVER_PATH = DRIVER_BIN  # 可以指定绝对路径，如果不指定的话会在$PATH里面查找

USE_PROXY = True

#################################

# mongodb
# MONGODB_HOST = "127.0.0.1"
# MONGODB_PORT = 27017

# DATABASE_NAME = 'common'
# mongodb_client = mongodb_service.get_client(MONGODB_HOST, MONGODB_PORT)
# mongodb = mongodb_service.get_db(mongodb_client, DATABASE_NAME)

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DATABASE_NAME = 0

# Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE_NAME)

# mysql
# mysql数据库连接信息
DATABASES = {
    'DRIVER': 'mysql+pymysql',
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'NAME': 'worm',
    'USER': 'root',
    'PASSWORD': 'root',
}
