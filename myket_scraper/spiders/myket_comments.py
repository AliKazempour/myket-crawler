import scrapy


class MyketCommentsSpider(scrapy.Spider):
    name = "myket_comments"
    allowed_domains = ["myket.ir"]
    start_urls = ["https://myket.ir"]

    def parse(self, response):
        pass
