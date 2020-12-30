# -*- coding: utf-8 -*-


import connect as con

import sys

reload(sys)
sys.setdefaultencoding('utf8')
base_url = 'http://travel.cntour.cn/'


# 获取banner
def banner():
    soup = con.connection(base_url)
    pic = soup.find('div', attrs={'class': 'pic'})
    ul = pic.find('ul')
    img = ul.findAll('img')
    for pcg in img:
        sql = "REPLACE INTO banner(path) VALUES ('%s')" % (
            base_url+pcg['src'])
        con.insert_data(sql)


banner()


img_list = []
title_list = []
browse_list = []
author_list = []


# 获取攻略
def raiders():
    for page in range(100):
        soup = con.connection(base_url + 'travels/list.aspx?cid=0&days=0&o=0&m=0&d1=0&d2=0&page=' + str(page + 1))
        # 获取图片
        pics_li = soup.findAll('li', attrs={'class': 'pics'})
        for pics in pics_li:
            img = pics.findAll('img')
            for src in img:
                img_list.append(base_url + src['src'])
        # 获取title
        title_li = soup.findAll('li', attrs={'class': 'title'})
        for title in title_li:
            for href in title.findAll('a'):
                title_list.append({
                    'title': title.getText(),
                    'href': href['href']
                })

        # 获取浏览人数
        data_li = soup.findAll('li', attrs={'class': 'data'})
        for data in data_li:
            p1 = data.find('span', attrs={'class': 'p1'})
            p2 = data.find('span', attrs={'class': 'p2'})
            p3 = data.find('span', attrs={'class': 'p3'})
            browse_list.append({
                "like": str(p1.getText()),
                "message": str(p2.getText()),
                "look": str(p3.getText()),
            })

        # 获取作者
        description_li = soup.findAll('li', attrs={'class': 'description clearfix'})
        for description in description_li:
            author_div = description.findAll('div')
            for author in author_div:
                for img in author.findAll('img'):
                    author_list.append({
                        'time': description.find('span').getText(),
                        'author': author.getText(),
                        'author_img': base_url + img['src']
                    })

# raiders()
#
# for index in range(len(img_list)):
#     raiders_img = img_list[index]
#     raiders_href = title_list[index]['href']
#     raiders_title = title_list[index]['title']
#     raiders_like = browse_list[index]['like']
#     raiders_message = browse_list[index]['message']
#     raiders_look = browse_list[index]['look']
#     raiders_author = author_list[index]['author']
#     raiders_authorImg = author_list[index]['author_img']
#     raiders_time = author_list[index]['time']
#
#     sql="REPLACE INTO raiders(raiders_img,raiders_href,raiders_title,raiders_like,raiders_message,raiders_look,raiders_author,raiders_authorImg,raiders_time) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
#                     raiders_img, raiders_href,raiders_title,raiders_like,raiders_message,raiders_look,raiders_author,raiders_authorImg,raiders_time)
#     con.insert_data(sql)
