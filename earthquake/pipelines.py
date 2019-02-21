# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class EarthquakePipeline(object):

    def __init__(self, hostname, username, password, database):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        # pull in information from settings.py
        return cls(
            hostname=crawler.settings.get("DB_HOSTNAME"),
            username=crawler.settings.get("DB_USERNAME"),
            password=crawler.settings.get("DB_PASSWORD"),
            database=crawler.settings.get("DB_NAME")
        )

    def open_spider(self, spider):
        self.connection = psycopg2.connect(
                host=self.hostname,
                user=self.username,
                password=self.password,
                dbname=self.database
            )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into "chartApp_earthquakereport"(time_occured,longitude,latitude,magnitude,depth,location) values(%s,%s,%s,%s,%s,%s)""",
                (
                    item['time_occured'],
                    item['longitude'],
                    item['latitude'],
                    item['magnitude'],
                    item['depth'],
                    item['location']
                )
            )
            self.connection.commit()
        except Exception as e:
            print(e)
        return item
