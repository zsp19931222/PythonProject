# -*- coding: utf-8 -*-

import connect as con
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, time
import multiprocessing
from time import sleep

from DBManager import DBManager

dbManager = DBManager()


def path():
    soup = con.connection('https://www.zhibo8.cc/zuqiu/more.htm?label=%E8%8B%B1%E8%B6%85')
    div = soup.find('div', attrs={'class': 'dataList'})
    a_list = div.findAll('a')
    for a in a_list:
        second_url = "https://www.zhibo8.cc/" + a['href']
        if second_url.endswith('svideo.htm'):
            open(second_url, a.getText())


def open(url, title=''):
    # chromedriver的绝对路径
    driver_path = r'D:\chromedriver\chromedriver.exe'
    # 初始化一个driver，并且指定chromedriver的路径
    driver = webdriver.Chrome(executable_path=driver_path)
    # 请求网页
    driver.get(url)
    # 通过page_source获取网页源代码
    res = driver.page_source
    soup = BeautifulSoup(res, "html.parser")
    try:
        video = soup.find('video')['src']
        img = soup.find('img', attrs={'class': 'thumb_img'})['src']
        sql = "REPLACE INTO %s(href,title,img,url) VALUES ('%s','%s','%s','%s')" % (
            'video', url, title, img, video)
        dbManager.insert(sql)
    except Exception as e:
        print(e)


# 程序运行时间在白天8:30 到 15:30  晚上20:30 到 凌晨 2:30
DAY_START = time(6, 30)
DAY_END = time(7, 30)

NIGHT_START = time(19, 30)
NIGHT_END = time(2, 30)


def run_child():
    while 1:
        path()


def run_parent():
    print("启动父进程")

    child_process = None  # 是否存在子进程

    while True:
        current_time = datetime.now().time()
        running = False  # 子进程是否可运行

        if DAY_START <= current_time <= DAY_END or (current_time >= NIGHT_START) or (current_time <= NIGHT_END):
            # 判断时候在可运行时间内
            running = True

        # 在时间段内则开启子进程
        if running and child_process is None:
            print("启动子进程")
            child_process = multiprocessing.Process(target=run_child)
            child_process.start()
            print("子进程启动成功")

        # 非记录时间则退出子进程
        if not running and child_process is not None:
            print("关闭子进程")
            child_process.terminate()
            child_process.join()
            child_process = None
            print("子进程关闭成功")

        sleep(5)


if __name__ == '__main__':
    run_parent()
