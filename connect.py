# -*- coding: utf-8 -*-

import json

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36'}


# 连接页面
def connection(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    return BeautifulSoup(res.text, "html.parser")


# 处理get请求携带的参数(从抓包工具中获取)
def get(url):
    # 2.发起基于ajax的post请求
    response = requests.get(url=url, headers=headers)
    # 获取响应内容：响应内容为json串
    data = response.text
    data = json.loads(data)
    return data


# 处理post请求携带的参数(从抓包工具中获取)
def post(url, data):
    # 2.发起基于ajax的post请求
    response = requests.post(url=url, data=data, headers=headers)
    # 获取响应内容：响应内容为json串
    data = response.text
    data = json.loads(data)
    return data
