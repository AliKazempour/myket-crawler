import os
import sys
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from myket_scraper.spiders.myket_comments import MyketCommentsSpider

load_dotenv()

def run_spider():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    # اجرای اسپایدر
    process.crawl(MyketCommentsSpider)
    process.start()

if __name__ == "__main__":
    run_spider()