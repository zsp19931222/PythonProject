# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors


class DBManager:
    def connect(self):
        self.conn = pymysql.connect(
            host='141.164.49.212',
            user='root',
            password='123456',
            db='sport_news',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            port=3306)

    def query(self, sql):
        self.connect()
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except pymysql.OperationalError:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        return cursor

    def insert(self, sql):
        try:
            cursor = self.query(sql)
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)

    def select(self, sql):
        try:
            cursor = self.query(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(e)
