# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy

@dataclass
class MyketScraperItem:
    # define the fields for your item here like:
    # name: str | None = None
    pass



class ReviewItem(scrapy.Item):
    comment_id = scrapy.Field()
    package_name = scrapy.Field()
    author_name = scrapy.Field()
    rating = scrapy.Field()
    comment_text = scrapy.Field()
    comment_date = scrapy.Field()
    reply_text = scrapy.Field()
    likes_count = scrapy.Field()
    dislikes_count = scrapy.Field()
    