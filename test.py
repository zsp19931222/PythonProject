# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pymysql


# 保存数据
def insert_data(sql):
    # 打开数据库连接
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='022875',
        db='tourism',
        charset='utf8'
    )
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
    # 关闭数据库连接
    db.close()


# 连接页面
def connection(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.88 Safari/537.36'}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    return BeautifulSoup(res.text, "html.parser")


# 获取全部要闻
def all_news():
    base_url = 'http://www.cntour.cn/news/list.aspx?tid=50&page='
    soup = connection(base_url)
    for page in range(int(
            soup.find('div', attrs={'class': 'pathBox'}).find('a', attrs={'class': 'text'}).getText().split('/')[1])):
        soup = connection(base_url + str(page + 1))
        news_div_list = soup.find("div", attrs={'newsList'})
        news_ul_list = news_div_list.find('ul')
        print news_ul_list.findAll('a')
        for index, news in enumerate(news_ul_list.findAll('a')):
            insert_data("REPLACE INTO news(news_title,news_href) VALUES ('%s','%s')" % (
                news.getText(), news['href']))


# all_news()


# 获取行业动态http://www.cntour.cn/news/list.aspx?tid=57
def all_dynamic():
    base_url = 'http://www.cntour.cn/news/list.aspx?tid=57&page='
    soup = connection(base_url)
    dynamic_div_page = soup.find('div', attrs={'class': 'pathBox'}).find('a', attrs={'class': 'text'}).getText().split('/')[1]
    for page in range(int(dynamic_div_page)):
        soup = connection(base_url + str(page + 1))
        dynamic_div_list = soup.find("div", attrs={'newsList'})
        dynamic_ul_list = dynamic_div_list.find('ul')
        print dynamic_ul_list.findAll('a')
        for index, dynamic in enumerate(dynamic_ul_list.findAll('a')):
            insert_data("REPLACE INTO dynamic(dynamic_title,dynamic_href) VALUES ('%s','%s')" % (
                dynamic.getText(), dynamic['href']))


# all_dynamic()

