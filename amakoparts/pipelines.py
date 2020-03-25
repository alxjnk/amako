# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# import psycopg2
import json
import pymysql

from scrapy import signals
from scrapy.exporters import CsvItemExporter

cur_man = 0;
class AmakopartsPipeline(object):
    def open_spider(self, spider):
        self.connection = pymysql.connect(
            '127.0.0.1', 'agronova_as', '_ccZ9a(f$wpB', 'agronova_bs')
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.execute("SELECT * FROM oc_product_related")
 
        # rows = self.cur.fetchall()
        # for row in rows:
        #     self.cur.execute("SELECT TOP 1 FROM oc_product WHERE oc.product.model = %s", (row['related_id']))
        #     id = self.cur.fetcone();
        #     self.cur.execute("INSERT INTO FROM oc_product_related () WHERE oc.product.model = %s", (row['related_id']))

        #     print(row["id"], row["name"])
          

        self.cur.close()
        self.connection.close()
    def process_item(self, item, spider):
        self.cur.execute(
            "SELECT * FROM oc_manufacturer WHERE name = %s", item['manufacturer'])

        result = self.cur.fetchone()
        print(result)
        if result == None:
            self.cur.execute("INSERT INTO oc_manufacturer (manufacturer_id, name, image) VALUES (%s, %s, %s)",
                             (item['manufacturer'].lower(), item['manufacturer'], item['manufacturer_img']))


        self.cur.execute("insert into oc_product ( image, manufacturer_id, price, quantity, SKU, model) VALUES (%s,%s,%s,%s,%s, %s)",
                         ( item['img_link'], item['manufacturer'].lower(), item['price'], item['quantity'], item['title'], item['title']))
        self.cur.execute("insert into oc_product_to_store ( store_id) VALUES (%s)",
                         (0))

        self.cur.execute("insert into oc_product_description ( name, description, meta_title, meta_description, language_id) VALUES (%s,%s,%s,%s,%s)",
                         ( item['title'], item['title'], item['title'],item['title'], 1))

        for product in item['replacements']:
            self.cur.execute("insert into oc_product_related ( product_id, related_id) VALUES (%s,%s)",
                             (item['title'], product))

        

        self.connection.commit()
        return item


# class CsvPipeline(object):
#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls()
#         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#         return pipeline

#     def spider_opened(self, spider):
#         self.file = open('output.csv', 'w+b')
#         self.exporter = CsvItemExporter(self.file)
#         self.exporter.start_exporting()

#     def spider_closed(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()

#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item

# import json

# class JsonWriterPipeline(object):

#     def open_spider(self, spider):
#         self.file = open('items.json', 'w', encoding="windows-1251")

#     def close_spider(self, spider):
#         self.file.close()

#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item
