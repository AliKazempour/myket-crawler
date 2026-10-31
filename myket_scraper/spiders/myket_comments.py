import hashlib
import os
import scrapy
from dotenv import load_dotenv
from myket_scraper.items import ReviewItem

load_dotenv()

def fa_to_en_digits(text: str) -> str:
    if not text:
        return "0"
    trans = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    return text.translate(trans).strip()

class MyketCommentsSpider(scrapy.Spider):
    name = "myket_comments"
    allowed_domains = ["myket.ir"]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.package_name = os.getenv("APP_PACKAGE_NAME") or "ir.shahbaz.SHZToolBox"
        self.start_urls = [f"https://myket.ir/app/{self.package_name}"]

    def parse(self, response):
        self.logger.info(f"Page response: {response.status}")
        comment_boxes = response.css("div.comment-wrapper div.comment-box")
        self.logger.info(f"Comment boxes: {len(comment_boxes)}")

        for box in comment_boxes:
            item = ReviewItem()
            item["package_name"] = self.package_name

            author = box.xpath(".//div[contains(@class, 'avatar-wrapper')]/span/text()").get()
            if not author:
                alt = box.css("img.avatar::attr(alt)").get() or ""
                author = alt.replace("عکس کاربر -", "").strip()
            item["author_name"] = author.strip() if author else "کاربر ناشناس"

            stars_text = box.css("span.rating-stars::text").get(default="").strip()
            item["rating"] = len(stars_text) if stars_text else 0

            item["comment_date"] = box.css("span.date::text").get(default="").strip()
            item["comment_text"] = box.xpath("./p/text()").get(default="").strip()

            likes_raw = box.xpath(".//div[contains(@class, 'comment-reaction')]/i[contains(@class, 'thumbs-up')]/following-sibling::span[1]/text()").get()
            dislikes_raw = box.xpath(".//div[contains(@class, 'comment-reaction')]/i[contains(@class, 'thumbs-down')]/following-sibling::span[1]/text()").get()

            item["likes_count"] = int(fa_to_en_digits(likes_raw)) if likes_raw else 0
            item["dislikes_count"] = int(fa_to_en_digits(dislikes_raw)) if dislikes_raw else 0

            reply = box.css("div.developer-reply p::text").get()
            item["reply_text"] = reply.strip() if reply else None

            unique_str = f"{self.package_name}_{item['author_name']}_{item['comment_date']}_{item['comment_text'][:20]}"
            item["comment_id"] = hashlib.md5(unique_str.encode("utf-8")).hexdigest()

            yield item