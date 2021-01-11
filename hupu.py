# -*- coding: utf-8 -*-


import connect as con
import re

from DBManager import DBManager

# url = 'https://soccer.hupu.com/'
dbManager = DBManager()


# def data():
#     table = 'hupu_soccer'
#     soup = con.connection(url)
#     div_list = soup.find('div', attrs={'class', 'list-area-main-infinite'})
#     a_list = div_list.findAll('a')
#     for a in a_list:
#         href = a['href']
#         title = a.find('div', attrs={'class', 'list-area-main-infinite-item-content-title'})
#         title_text = title.getText().strip()
#         print(title_text)
#         aside = a.find('aside', attrs={'class', 'list-area-main-infinite-item-aside'})
#         if aside is None:
#             img = ''
#         else:
#             p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配
#             img = re.findall(p1, aside['style'])[0]
#         sql = "REPLACE INTO %s(href,title,img) VALUES ('%s','%s','%s')" % (
#             table, href, title_text, img)
#         dbManager.insert(sql)

def api(page=1):
    for i in range(page):
        data_list = con.get('https://soccer.hupu.com/api/v1/fifa?p=%s' % i)
        for data in data_list['data']:
            print(data['title'])
            if data['hasImg']:
                img = data['img']
            else:
                img = ''
            sql = "REPLACE INTO %s(href,title,img) VALUES ('%s','%s','%s')" % (
                'hupu_soccer', data['url'], data['title'], img)
            dbManager.insert(sql)
