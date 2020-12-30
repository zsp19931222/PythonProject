# -*- coding: utf-8 -*-
import connect as con


# 获取全部要闻
def all_news():
    base_url = 'http://www.cntour.cn/news/list.aspx?tid=50&page='
    soup = con.connection(base_url)
    for page in range(int(
            soup.find('div', attrs={'class': 'pathBox'}).find('a', attrs={'class': 'text'}).getText().split('/')[1])):
        soup = con.connection(base_url + str(page + 1))
        news_div_list = soup.find("div", attrs={'newsList'})
        news_ul_list = news_div_list.find('ul')
        print news_ul_list.findAll('a')
        for index, news in enumerate(news_ul_list.findAll('a')):
            con.insert_data("REPLACE INTO news(news_title,news_href) VALUES ('%s','%s')" % (
                news.getText(), news['href']))


# all_news()


# 获取行业动态http://www.cntour.cn/news/list.aspx?tid=57
def all_dynamic():
    base_url = 'http://www.cntour.cn/news/list.aspx?tid=57&page='
    soup = con.connection(base_url)
    dynamic_div_page = \
    soup.find('div', attrs={'class': 'pathBox'}).find('a', attrs={'class': 'text'}).getText().split('/')[1]
    for page in range(int(dynamic_div_page)):
        soup = con.connection(base_url + str(page + 1))
        dynamic_div_list = soup.find("div", attrs={'newsList'})
        dynamic_ul_list = dynamic_div_list.find('ul')
        print dynamic_ul_list.findAll('a')
        for index, dynamic in enumerate(dynamic_ul_list.findAll('a')):
            con.insert_data("REPLACE INTO dynamic(dynamic_title,dynamic_href) VALUES ('%s','%s')" % (
                dynamic.getText(), dynamic['href']))

# all_dynamic()
