# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import psycopg2
import json

from scrapy import signals
from scrapy.exporters import CsvItemExporter


# class AmakopartsPipeline(object):
#     def open_spider(self, spider):
#         hostname = 'balarama.db.elephantsql.com'
#         username = 'nmnwuopl' # the username when you create the database
#         password = 'O6eGuGRaw1iqOeU4xecihU0kESQkRhUo' #change to your password
#         database = 'nmnwuopl'
#         self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
#         self.cur = self.connection.cursor()

#     def close_spider(self, spider):
#         self.cur.close()
#         self.connection.close()

#     def process_item(self, item, spider):
#         print(item)
#         self.cur.execute("insert into amako(DT_RowId,img_link,manufacturer,manufacturerid,partid,price,quantity,replacements,title) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#         (item['DT_RowId'],item['img_link'],item['manufacturer'],item['manufacturerid'],item['partid'],item['price'],item['quantity'],json.dumps(item['replacements']),item['title']))
#         self.connection.commit()
#         return item


# class CsvPipeline(object):
#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls()
#         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#         return pipeline

#     def spider_opened(self, spider):
#         self.file = open('output.csv', 'w+', encoding="windows-1251")
#         self.exporter = CsvItemExporter(self.file)
#         self.exporter.start_exporting()

#     def spider_closed(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()

#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item

import json

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'w', encoding="windows-1251")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item