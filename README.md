<div dir="rtl">

# سامانه استخراج و ذخیره‌سازی خودکار نظرات اپلیکیشن «جعبه ابزار» از مایکت

این پروژه به طور اختصاصی برای **استخراج، پردازش و پایش دوره‌ای نظرات کاربران اپلیکیشن «جعبه ابزار» از مارکت مایکت** پیاده‌سازی شده است. داده‌های استخراج‌شده پس از اعتبارسنجی و تولید شناسه یکتا، به صورت خودکار در پایگاه داده PostgreSQL ذخیره شده و از رکوردهای تکراری جلوگیری می‌شود.

---

## ویژگی‌های فنی و عملیاتی

* **استخراج نظرات جعبه ابزار:** دریافت نام کاربر، امتیاز، تاریخ، متن نظر، لایک/دیس‌لایک و پاسخ توسعه‌دهنده.
* **ذخیره‌سازی در PostgreSQL:** تولید شناسه با `MD5` و استفاده از Upsert برای جلوگیری از تکرار و به‌روزرسانی نظرات.
* **اجرای محلی یا با Docker Compose:** راه‌اندازی اسکرپر و پایگاه داده متناسب با محیط اجرا.
* **اجرای خودکار و ثبت لاگ:** زمان‌بندی با `cron` برای هر جمعه ساعت ۳:۰۰ بامداد.

## ساختار جدول در پایگاه داده (`myket_reviews`)

| فیلد | نوع داده | توضیحات |
| --- | --- | --- |
| `comment_id` | `VARCHAR(64)` | کلید اصلی جدول |
| `package_name` | `VARCHAR(150)` | شناسه پکیج برنامه  |
| `author_name` | `VARCHAR(255)` | نام کاربر ثبت‌کننده نظر |
| `rating` | `SMALLINT` | امتیاز کاربر بین ۱ تا ۵ ستاره |
| `comment_text` | `TEXT` | متن کامل دیدگاه ثبت‌شده |
| `comment_date` | `VARCHAR(100)` | تاریخ ثبت نظر در مایکت |
| `likes_count` | `INTEGER` | تعداد لایک‌های دریافتی |
| `dislikes_count` | `INTEGER` | تعداد دیس‌لایک‌های دریافتی |
| `reply_text` | `TEXT` | پاسخ رسمی تیم پشتیبانی «جعبه ابزار» (در صورت وجود) |
| `created_at` | `TIMESTAMPTZ` | زمان اولین ثبت رکورد در پایگاه داده |
| `updated_at` | `TIMESTAMPTZ` | زمان آخرین همگام‌سازی یا تغییر وضعیت نظر |

## تنظیم متغیرهای محیطی (`.env`)

قبل از شروع، یک نسخه از روی فایل `.env.example` با نام `.env` بسازید:

```bash
cp .env.example .env
```

مقادیر را مطابق نمونه تنظیم نمایید:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myket_reviews_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
APP_PACKAGE_NAME=ir.shahbaz.SHZToolBox
```

## راه‌اندازی با Docker Compose (روش پیشنهادی)

تمامی نیازمندی‌ها شامل سرویس پایگاه داده و خودکارسازی اسکرپر در داکر تعبیه شده است. برای جلوگیری از تداخل پورت با سرویس‌های احتمالی لینوکس، پورت خارجی دیتابیس بر روی 5433 نگاشت شده است.

### ۱. ساخت ایمیج‌ها و اجرای سرویس‌ها:

```bash
docker compose up --build
```

### ۲. بررسی رکوردهای ذخیره‌شده درون دیتابیس کانتینر:

```bash
docker compose exec db psql -U postgres -d myket_reviews_db -c "SELECT comment_id, author_name, rating, likes_count FROM myket_reviews LIMIT 5;"
```

### ۳. اجرای مجدد اسکرپر برای به‌روزرسانی نظرات:

```bash
docker compose run --rm crawler
```

### ۴. خاموش کردن کانتینرها (با حفظ داده‌ها):

```bash
docker compose down
```

## راه‌اندازی و اجرای محلی (بدون Docker)

در صورتی که قصد دارید پروژه را مستقیماً روی سیستم‌عامل میزبان اجرا کنید:

### ۱. ساخت و فعال‌سازی محیط مجازی پایتون:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ۲. ایجاد دیتابیس و اجرای جدول SQL:

```bash
# Create the local database
sudo -u postgres psql -c "CREATE DATABASE myket_reviews_db;"

# Create the reviews table
sudo -u postgres psql -d myket_reviews_db -f sql/init_reviews.sql
```

### ۳. اجرای اسکرپر:

```bash
# Run with Scrapy
scrapy crawl myket_comments

# Or use the Python runner
python runner.py
```

## زمان‌بندی خودکار دوره‌ای (Cron Job)

برای اجرا **هر جمعه ساعت ۳:۰۰ بامداد به وقت سیستم**، ابتدا مجوز اجرای اسکریپت را بدهید:

```bash
chmod +x run_crawler.sh
crontab -e
```

خط زیر را با مسیر مطلق پروژه اضافه کنید. لاگ‌ها در `logs/crawler.log` ذخیره می‌شوند:

```cron
0 3 * * 5 /path/to/project/run_crawler.sh
```

</div>
