# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from mysql.connector import errorcode


class SczfcgPipeline(object):
    add_record = ("INSERT INTO sczfcg "
                  "(project_name,procurement_method)"
                  "VALUES (%s, %s)")

    def open_spider(self, spider):
        try:
            self.cnx = mysql.connector.connect(user='root', password='18148411316',
                                               host='127.0.0.1',
                                               database='swust')
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close_spider(self, spider):
        self.cursor.close()
        self.cnx.close()

    def process_item(self, item, spider):
        try:
            data_record = (item['projectName'], item['procurementMethod'])
            self.cursor.execute(self.add_record, data_record)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print (err)
        return item
