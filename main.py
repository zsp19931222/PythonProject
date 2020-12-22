# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 15:37:41 2018

@author: ASUS
"""

import requests
from bs4 import BeautifulSoup
# import pandas as pd
import re


# 获取所有网页的地址
def make_url_list():
    url_list = []

    url = 'https://movie.douban.com/top250?start='
    step = 25
    for i in range(10):
        res = url + str(i * step)
        url_list.append(res)
    return url_list


url_list = make_url_list()

# 设定所需的5列数据：电影排名、电影名称、电影评分、评论人数、短评
total_rank_list = []
total_movie_name = []
total_movie_score = []
total_comment_num = []
total_quote_list = []
total_img_list = []
total_time_list = []

for url in url_list:
    # 设定每次循环所需的5列数据：电影排名、电影名称、电影评分、评论人数、短评
    movie_name = []
    comment_num = []
    quote_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

    res = requests.get(url, headers=headers)
    # 下载一个网页

    res.raise_for_status()
    res.encoding = 'utf-8'

    '''获取一个网页包含的电影排名、电影名称、电影评分、评论人数、短评。其中，电影排名、
电影评分、短评的属性是唯一的，直接用BeautifulSoup里的select方法选出，生成list'''

    soup = BeautifulSoup(res.text, "html.parser")
    rank = soup.select('em')
    rank_list = [i.getText() for i in rank]

    score = soup.select('.rating_num')
    movie_score = [j.getText() for j in score]

    '''电影名称和评论人数的属性不是唯一的，电影名称使用BeautifulSoup里的find选出第一个匹配值，
评论人数先用find找出所在的标签属性，再用正则表达式匹配倒数第一位数字. 短评属性唯一,但存在空值,
因此用find选出每次的匹配值'''

    movie_list = soup.find('ol', attrs={'class': 'grid_view'})
    for movie in movie_list.find_all('li'):

        name = movie.find('span', attrs={'class': 'title'}).getText()
        movie_name.append(name)

        imgs = movie.find_all('img')
        for img in imgs:
            total_img_list.append(img['src'])

        time = movie.find('p', attrs={'class': ''}).getText().split('主演'.decode('utf8'))
        try:
            print (time[1].split('...')[1].strip())
        except:
            print ()


        total_time_list.append(time[0].strip())

        comment_info = movie.find('div', attrs={'class': 'star'})
        num = re.findall(r'\d+', str(comment_info))[-1]
        comment_num.append(num)

        quote = movie.find('span', attrs={'class': 'inq'})
        if quote is not None:
            quote_list.append(quote.getText())
        else:
            quote_list.append('无')

    '''将每次循环得到的列表加到总列表里'''
    total_rank_list.extend(rank_list)
    total_movie_name.extend(movie_name)
    total_movie_score.extend(movie_score)
    total_comment_num.extend(comment_num)
    total_quote_list.extend(quote_list)

# 用pandas输出为csv格式的文件
data = {'电影排名': total_rank_list, '电影名称': total_movie_name, \
        '电影评分': total_movie_score, '评论人数': total_comment_num, \
        '短评': total_quote_list}

for index in range(len(total_movie_name)):
    print ("<---------------------------->")
    print (total_rank_list[index])
    print (total_movie_name[index])
    print (total_movie_score[index])
    print (total_comment_num[index])
    print (total_quote_list[index])
    print (total_img_list[index])
    print (total_time_list[index])
# df = pd.DataFrame(data)
# df.to_csv('douban_movie.csv', index=False)
