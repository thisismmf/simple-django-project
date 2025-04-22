# simple-django-project

سلام! من این پروژه ساده‌ی **Login/Registration** رو با Django و Django REST framework پیاده کردم. هدف اصلی این پروژه شبیه‌سازی فرایند ورود و ثبت‌نام با شماره موبایل و کد تایید یکبار مصرف (OTP) هست، به‌همراه محدود کردن درخواست‌های مشکوک از یک IP.

## ⚙️ نیازمندی‌ها

- Python 3.8+
- pip (یا pipenv/poetry)
- virtualenv (یا ابزار مدیریت محیط مجازی مورد علاقه شما)
- Django
- Django REST framework
- drf-yasg (برای مستندات API)

---

## 🛠️ راه‌اندازی محیط توسعه

1.  **کلون کردن مخزن**
    ```bash
    git clone <repository_url>
    cd simple-django-project
    ```

2.  **ایجاد و فعال‌سازی virtualenv**
    ```bash
    python -m venv venv
    source venv/bin/activate      # در Mac/Linux
    # .\venv\Scripts\activate    # در Windows
    ```

3.  **نصب وابستگی‌ها**
    ```bash
    pip install -r requirements.txt
    ```
    *(اگر فایل `requirements.txt` وجود ندارد، آن را با دستور `pip freeze > requirements.txt` ایجاد کنید یا وابستگی‌ها را دستی نصب کنید: `pip install django djangorestframework drf-yasg`)*

4.  **اجرای مایگریشن‌ها**
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

| مسیر                     | روش | ورودی (JSON)                                                                       | خروجی موفق (JSON)                                      | توضیحات                                                                 |
| :------------------------ | :--- | :---------------------------------------------------------------------------------- | :----------------------------------------------------- | :----------------------------------------------------------------------- |
| `/mobile/`                | POST | `{ "mobile": "+1234567890" }`                                                     | `{ "detail": "Verification code sent." }` (201) یا `{ "registered": true }` (200) | ارسال کد تایید برای کاربر جدید یا اطلاع از ثبت‌نام قبلی کاربر.           |
| `/verify-code/`           | POST | `{ "mobile": "+1234567890", "code": "123456" }`                                    | `{ "detail": "Code verified. Proceed to registration." }` | بررسی کد تایید ارسال شده.                                                |
| `/complete-registration/` | POST | `{ "mobile": "+1234567890", "full_name": "...", "email": "...", "password": "..." }` | `{ "detail": "Registration complete." }`                | تکمیل اطلاعات ثبت‌نام کاربر پس از تایید کد.                             |
| `/login/`                 | POST | `{ "mobile": "+1234567890", "password": "..." }`                                   | `{ "detail": "Login successful." }`                     | ورود کاربر با شماره موبایل و رمز عبور.                                   |

### مستندات Swagger/ReDoc

برای مشاهده مستندات تعاملی API از طریق Swagger UI یا ReDoc، پس از اجرای سرور، به آدرس‌های زیر مراجعه کنید:

-   **Swagger UI**: `http://127.0.0.1:8000/swagger/`
-   **ReDoc**: `http://127.0.0.1:8000/redoc/`

---

## 🔒 محدودیت‌های امنیتی (Rate Limiting)

-   **ثبت‌نام**: اگر از یک IP مشخص، ۳ درخواست ثبت‌نام با شماره‌های **متفاوت** ارسال شود که هنوز کد آن‌ها تایید نشده، آن IP به مدت ۱ ساعت مسدود می‌شود.
-   **ورود**: اگر از یک IP مشخص، ۳ تلاش ناموفق برای ورود (رمز عبور اشتباه) انجام شود، آن IP به مدت ۱ ساعت مسدود می‌شود.

*(این محدودیت‌ها با استفاده از Cache (in-memory) پیاده‌سازی شده‌اند و با ری‌استارت شدن سرور ریست می‌شوند.)*

---

## ✅ اجرای تست‌ها

```bash
python manage.py test tests.test_views
```

---
