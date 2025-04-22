# simple-django-project

سلام! من این پروژه ساده‌ی **Login/Registration** رو با Django پیاده کردم. هدف اصلی این پروژه شبیه‌سازی فرایند ورود و ثبت‌نام هست، به‌همراه محدود کردن درخواست‌های مشکوک از یک IP.

## ⚙️ نیازمندی‌ها

- Python 3.8+
- pip (یا pipenv/poetry)
- virtualenv (یا ابزار مدیریت محیط مجازی مورد علاقه شما)

---

## 🛠️ راه‌اندازی محیط توسعه

1. **کلون کردن مخزن**  
   ```bash
   git clone <repository_url>
   cd simple-django-project
   ```

2. **ایجاد و فعال‌سازی virtualenv**  
   ```bash
   python -m venv venv
   source venv/bin/activate      # در Mac/Linux
   # .\venv\Scripts\activate    # در Windows
   ```

3. **نصب وابستگی‌ها**  
   ```bash
   pip install -r requirements.txt
   ```

4. **اجرای مایگریشن‌ها**  
   ```bash
   python manage.py migrate
   ```

---

## 🚀 اجرای سرور لوکال

```bash
python manage.py runserver
```

---

## 🔑 مستندات API

تمامی مسیرها با پیشوند `/api/auth/` تعریف شدند. از JSON برای ارسال و دریافت داده استفاده کنید.

| مسیر       | روش | ورودی (JSON) | خروجی (JSON) | توضیحات |
|------------|-----|---------------|----------------|----------|
| `/request/` | POST | `{ "mobile": "09121112233" }` | `{ "detail": "Challenge created", "flow": "otp"}` | اگر کاربر جدید باشد `flow=otp`، در غیر این صورت `flow=password` |
| `/verify/` | POST | `{ "mobile": "...", "code": "123456" }` یا `{ "mobile": "...", "password": "pwd" }` | `{ "detail": "Verified" }` | بررسی کد یا پسورد |
| `/register/` | POST | `{ "mobile": "...", "full_name": "...", "email": "...", "password": "pwd" }` | `{ "detail": "Registration complete" }` | ثبت‌نام |
| `/login/` | POST | `{ "mobile": "...", "password": "pwd" }` | `{ "detail": "Login successful" }` | ورود |

---

## 🔒 محدودیت‌های امنیتی

- حداکثر ۳ تلاش ناموفق → مسدود شدن IP به مدت ۱ ساعت  
- ۳ درخواست ثبت‌نام ناموفق با شماره‌های متفاوت → مسدودسازی آن IP

---

## ✅ اجرای تست‌ها

```bash
python manage.py test
```

---
