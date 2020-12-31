# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import pymysql
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.88 Safari/537.36'}

db = pymysql.connect(
    host='141.164.49.212',
    port=3306,
    user='root',
    password='123456',
    db='sport_news',
    charset='utf8'
)


# 保存数据
def insert_data(sql):
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except Exception as ex:
        print (ex)
        # 如果发生错误则回滚
        db.rollback()


# 是否存在该数据
def has_data(select_sql):
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(select_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) > 0:
            b = bool(1)
        else:
            b = bool(0)
    except Exception as ex:
        print (ex)
        # 如果发生错误则回滚
        db.rollback()
        b = bool(0)

    return b


def select_data(select_sql):
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(select_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except Exception as ex:
        print (ex)
        # 如果发生错误则回滚
        db.rollback()
        results = ''
    print
    return results


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
