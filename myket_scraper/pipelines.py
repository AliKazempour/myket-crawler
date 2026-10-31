# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class MyketScraperPipeline:
#     def process_item(self, item):
#         return item

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class PostgresPipeline:
    def open_spider(self):
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = int(os.getenv("DB_PORT", 5432))
        db_name = os.getenv("DB_NAME", "myket_reviews_db")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "123456")

        self.conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        self.cur = self.conn.cursor()

    def process_item(self, item):
        query = """
            INSERT INTO myket_reviews (
                comment_id, package_name, author_name, rating,
                comment_text, comment_date, likes_count, dislikes_count, reply_text
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (comment_id) DO UPDATE SET
                likes_count = EXCLUDED.likes_count,
                dislikes_count = EXCLUDED.dislikes_count,
                reply_text = EXCLUDED.reply_text,
                updated_at = CURRENT_TIMESTAMP;
        """
        self.cur.execute(query, (
            item["comment_id"],
            item["package_name"],
            item["author_name"],
            item["rating"],
            item["comment_text"],
            item["comment_date"],
            item["likes_count"],
            item["dislikes_count"],
            item.get("reply_text")
        ))
        self.conn.commit()
        return item

    def close_spider(self):
        if hasattr(self, "cur") and self.cur:
            self.cur.close()
        if hasattr(self, "conn") and self.conn:
            self.conn.close()