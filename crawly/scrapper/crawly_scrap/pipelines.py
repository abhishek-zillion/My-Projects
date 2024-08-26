# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from psycopg2 import OperationalError
import psycopg2
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class WalmartPipeline:
    def process_item(self, item, spider):
        print(f"Processing item in WalmartPipeline: {item['url']}")
        if spider.name == 'walmart':
            adapter = ItemAdapter(item)
            adapter['url'] = adapter['url'].strip()
        return item


class SaveToPostgresPipeline:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host='localhost',
                user='postgres',
                password='celsius',
                dbname='walmart'
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS walmart_data (
                    id SERIAL PRIMARY KEY,
                    url VARCHAR(1024) NOT NULL UNIQUE
                )
            """)
            self.conn.commit()
        except OperationalError as e:
            print(f"Error connecting to the database: {e}")
            self.conn = None

    def process_item(self, item, spider):
        if not self.conn:
            return item  # Skip processing if the connection is not established

        adapter = ItemAdapter(item)
        try:
            self.cursor.execute(""" 
                INSERT INTO walmart_data (url) VALUES (%s)
            """, (adapter['url'].strip(),))
            self.conn.commit()
        except psycopg2.IntegrityError:
            self.conn.rollback()  # Rollback the transaction on error
            print(f"Duplicate URL found and skipped: {adapter['url']}")
            raise DropItem(
                f"Duplicate URL found and skipped: {adapter['url']}")
        except Exception as e:
            self.conn.rollback()  # Rollback the transaction on error
            print(f"Error saving item to database: {e}")
        return item

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
