# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class MyketScraperPipeline:
#     def process_item(self, item):
#         return item

import psycopg2
from scrapy.utils.project import get_project_settings

class PostgresPipeline:
    def open_spider(self, spider):
        settings = spider.settings
        self.conn = psycopg2.connect(
            host=settings.get("DB_HOST", "localhost"),
            port=settings.getint("DB_PORT", 5432),
            dbname=settings.get("DB_NAME", "myket_reviews_db"),
            user=settings.get("DB_USER", "postgres"),
            password=settings.get("DB_PASSWORD", "postgres")
        )
        self.cur = self.conn.cursor()
        spider.logger.info("Connected to PostgreSQL successfully.")

    def process_item(self, item, spider):
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

    def close_spider(self, spider):
        if hasattr(self, "cur") and self.cur:
            self.cur.close()
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
        spider.logger.info("PostgreSQL connection closed.")
