# -*- coding: utf-8 -*-


import connect as con
import time
import schedule

base_url = 'https://news.baidu.com/sports'
other_id = ['WorldSoccerNews', 'ChinaSoccerNews', 'OtherNews', 'CbaNews', 'LatestNews']


# other_id = ['OtherNews']
def save_data(table, a_list):
    for a in a_list:
        try:
            href = a['href']
        except Exception as e:
            print e
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
        select_sql = "select href from %s where href='%s'" % (table, href)
        if not con.has_data('sport_news', select_sql):
            sql = "REPLACE INTO %s(href,title,img) VALUES ('%s','%s','%s')" % (
                table, href, title, img)
            con.insert_data(sql, 'sport_news')
        delete_sql = "DELETE FROM %s where title='%s' or title= '%s' or title = '%s'" % (
            table, '更多'.decode('utf8'), '推荐阅读'.decode('utf8'), '精品推荐'.decode('utf8'))
        con.insert_data(delete_sql, 'sport_news')


def news_world_soccer():
    for other in other_id:
        other_url = 'https://news.baidu.com/widget?id=%s&channel=sports&t=%s' % (other, str(
            int(round(time.time() * 1000))))
        print other_url
        if other is 'WorldSoccerNews':
            table = 'world_soccer'
        elif other is 'ChinaSoccerNews':
            table = 'china_soccer'
        elif other is 'CbaNews':
            table = 'cba'
        elif other is 'OtherNews':
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


schedule.every(30).minutes.do(news_world_soccer)
schedule.every(30).minutes.do(nba)


while True:
    schedule.run_pending()  # 运行所有可以运行的任务
    time.sleep(1)
