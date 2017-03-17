# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymysql.cursors


class HomelinkPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            charset='utf8',
            use_unicode=False
        )

    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        sql = 'insert into lianjia.data(title,address,avgPrice,property,chaoxiang,sjtime,xiaoqu,quyu,count,xqid,totalcount,area) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        try:
            cursor.execute(sql, (
            item['title'], item['address'], item['avgPrice'], item['property'], item['chaoxiang'], item['sjtime'],
            item['xiaoqu'], item['quyu'], item['count'], item['xqid'], item['totalcount'], item['area']))
            self.conn.commit()
        except Exception, e:
            print e
            self.conn.rollback()

        return item
