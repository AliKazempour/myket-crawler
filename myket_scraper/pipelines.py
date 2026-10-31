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


class PostgresPipeline:

  def __init__(self, db_settings):
    self.db_settings = db_settings
    self.conn = None
    self.cur = None

  @classmethod
  def from_crawler(cls, crawler):
    settings = crawler.settings
    db_settings = {
        "host": settings.get("DB_HOST", "localhost"),
        "port": settings.getint("DB_PORT", 5432),
        "dbname": settings.get("DB_NAME", "myket_reviews_db"),
        "user": settings.get("DB_USER", "postgres"),
        "password": settings.get("DB_PASSWORD", "postgres"),
    }
    return cls(db_settings)

  def open_spider(self):
    self.conn = psycopg2.connect(**self.db_settings)
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
    self.cur.execute(
        query,
        (
            item["comment_id"],
            item["package_name"],
            item["author_name"],
            item["rating"],
            item["comment_text"],
            item["comment_date"],
            item["likes_count"],
            item["dislikes_count"],
            item.get("reply_text"),
        ),
    )
    self.conn.commit()
    return item

  def close_spider(self):
    if self.cur:
      self.cur.close()
    if self.conn:
      self.conn.close()