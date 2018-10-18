#!/usr/bin/python
# coding:utf-8

import selenium
import requests
import json
import os
from fake_useragent import UserAgent
import re

ua = UserAgent()

from selenium import webdriver

if __name__ == '__main__':
    url = 'https://www.zhihu.com/question/35547395'

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "../bin/win/chromedriver.exe")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 设置无界面
    options.add_argument('User-Agent' + ua.random)

    driver = webdriver.Chrome(chrome_options=options, executable_path=DRIVER_BIN)

    driver.get(url=url)

    with open('../dianping01.html', 'w', encoding='utf-8') as fp:
        fp.write(driver.page_source)

    driver.quit()
