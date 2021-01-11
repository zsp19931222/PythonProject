# -*- coding: utf-8 -*-


import random
import time
import schedule
import connect as con
import hupu
import push
from DBManager import DBManager

base_url = 'https://news.baidu.com/sports'
other_id = ['WorldSoccerNews', 'ChinaSoccerNews', 'OtherNews', 'CbaNews', 'LatestNews']
# other_id = ['CbaNews']

dbManager = DBManager()


# other_id = ['OtherNews']
def save_data(table, a_list):
    for a in a_list:
        try:
            href = a['href']
        except Exception as e:
            print(e)
        try:
            if href.startswith('http://baijiahao.baidu.com/'):
                second_soup = con.connection(a['href'])
                title = second_soup.find('h2').getText()
            else:
                title = a.getText()
        except:
            title = a.getText()
        try:
            img = second_soup.find('img', attrs={'class': 'large'})['src']
        except:
            img = ''
        if title == '':
            break

        sql = "REPLACE INTO %s(href,title,img) VALUES ('%s','%s','%s')" % (
            table, href, title, img)
        dbManager.insert(sql)
        delete_sql = "DELETE FROM %s where title='%s' or title= '%s' or title = '%s'" % (
            table, '更多', '推荐阅读', '精品推荐')
        dbManager.insert(delete_sql)


def push_message():
    table = ''
    title = ''
    i = random.randint(0, 6)
    if i == 0:
        table = 'world_soccer'
        title = '国际足球'

    elif i == 1:
        table = 'china_soccer'
        title = '国内足球'

    elif i == 2:
        table = 'cba'
        title = 'CBA'

    elif i == 3:
        table = 'nba'
        title = 'NBA'

    elif i == 4:
        table = 'latest'
        title = '最新新闻'

    elif i == 5:
        table = 'other'
        title = '综合新闻'
    elif i == 6:
        table = 'hupu_soccer'
        title = '虎扑足球'
    print(table)

    result = dbManager.select("select * from %s  order by id DESC limit 1" % table)
    if result != '':
        for data in result:
            push.all(data['title'], title, data['img'])


def news_world_soccer():
    for other in other_id:
        other_url = 'https://news.baidu.com/widget?id=%s&channel=sports&t=%s' % (other, str(
            int(round(time.time() * 1000))))
        print(other_url)
        if other == 'WorldSoccerNews':
            table = 'world_soccer'
        elif other == 'ChinaSoccerNews':
            table = 'china_soccer'
        elif other == 'CbaNews':
            table = 'cba'
        elif other == 'OtherNews':
            table = 'other'
        else:
            table = 'latest'
        soup = con.connection(other_url)
        a_list = soup.findAll('a')
        save_data(table, a_list)


def nba():
    soup = con.connection(base_url)
    div = soup.find('div', attrs={'class': 'column clearfix', 'id': 'col_nba'})
    a_list = div.findAll('a')
    save_data('nba', a_list)

    col_focus = soup.find('div', attrs={'class': 'column clearfix', 'id': 'col_focus'})
    a_list = col_focus.findAll('a')
    save_data('other', a_list)


schedule.every(5).minutes.do(news_world_soccer)
schedule.every(5).minutes.do(nba)
schedule.every(5).minutes.do(hupu.api)
schedule.every(30).minutes.do(push_message)
#
while True:
    schedule.run_pending()  # 运行所有可以运行的任务
    time.sleep(1)

# news_world_soccer()
# nba()
# push_message()

