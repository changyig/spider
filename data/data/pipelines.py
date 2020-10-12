# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class DataPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="scrapy",
            user="root",
            passwd="root",
            charset='utf8',
            use_unicode=True
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()


    def open_spider(self, spider):
        # 关闭游标和连接
        print('开启蜘蛛')


    def process_item(self, item, spider):
        sql = "INSERT INTO keyword(keyword,info,url,createtime) VALUES(%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql, (item['keyword'], item['info'], item['url'], item['createtime']))
            self.cursor.connection.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
        return item


    def close_spider(self, spider):
        # 关闭游标和连接
        print('关闭蜘蛛')
        self.cursor.close()
        self.connect.close()
