# راهنمای نصب کامل پلاگین بله

هدف: نصب و بارگذاری صحیح پلاگین بله روی Hermes Agent، از گرفتن کد تا تأیید نهایی که ربات کار می‌کند.

---

## پیش‌نیازها

- **Hermes Agent** نصب‌شده با pip یا از ریپازیتوری (نسخه ۱.۰ یا بالاتر)
- **Python 3.10+** با `python3` و `pip`
- **پکیج `python-telegram-bot`** — این پلاگین از آن استفاده می‌کند (با استثنای `httpx`)
- یک **ربات بله** با توکن (از [@botfather](https://ble.ir/botfather) بگیرید)

> این پلاگین مستقل است و باید در فهرست پلاگین‌های کاربری Hermes کپی شود — به‌صورت
> خودکار همراه Hermes نصب نمی‌شود.

---

## مراحل

### مرحله ۱: کد پلاگین را به‌دست آورید

دو راه دارید:

**راه الف — کلون از GitHub (پیشنهادی):**

```bash
git clone https://github.com/Amirezamky9/hermes-bale-adapter.git
```

سپس محتوای پوشه را به فهرست پلاگین‌های هرمس منتقل کنید:

```bash
mkdir -p ~/.hermes/plugins/platforms/bale
cp -r hermes-bale-adapter/* ~/.hermes/plugins/platforms/bale/
```

**راه ب — کپی دستی:** اگر کد را جداگانه دارید، همین فایل‌ها را در
`~/.hermes/plugins/platforms/bale/` قرار دهید.

در انتها ساختار باید شبیه این باشد:

```
~/.hermes/plugins/platforms/bale/
├── __init__.py
├── adapter.py
├── bale_ids.py
├── bale_network.py
├── plugin.yaml
├── .env.example
└── tests/
    └── test_adapter.py
```

### مرحله ۲: پکیج موردنیاز را نصب کنید

در محیط پایتونِ هرمس (همان venv که Hermes استفاده می‌کند):

```bash
pip install python-telegram-bot httpx
```

تأیید نصب:

```bash
python3 -c "import telegram; print(telegram.__version__)"
```

### مرحله ۳: توکن بله را در فایل نمونه تنظیم کنید

```bash
cd ~/.hermes/plugins/platforms/bale
cp .env.example .env
```

`.env` را ویرایش کنید:

```bash
BALE_BOT_TOKEN=123456789:ABCdef123GHIklm456NOPqrs789TUVwxyz01
```

### مرحله ۴: پلاگین را در config.yaml فعال کنید

فایل `~/.hermes/config.yaml` را باز کنید. دو کار انجام دهید:

**الف)** در بخش `gateway.platforms`، بلوک `bale` را اضافه کنید:

```yaml
gateway:
  platforms:
    bale:
      enabled: true
      token: 123456789:ABCdef123GHIklm456NOPqrs789TUVwxyz01
      extra:
        allow_from:
          - '66881162'
      home_channel:
        chat_id: '66881162'
        name: پیام شخصی
```

**ب)** در بخش `plugins.enabled`، پلاگین را لیست کنید:

```yaml
plugins:
  enabled:
    - platforms/bale
```

> ⚠️ نکتهٔ مهم: اگر یک بلوک `bale` در سطح بالای `platforms:` هم دارید، مطمئن شوید
> `enabled: true` است. در غیر این صورت مقدار تکراری `enabled: false` تنظیمات
> gateway را نادیده می‌گیرد (یک مشکل شناخته‌شده در همین پروژه بود).

### مرحله ۵: گیت‌وی را ری‌استارت کنید

```bash
hermes gateway restart
```

اگر Hermes در داکر یا systemd اجرا می‌شود، طبق همان محیط ری‌استارت کنید.

### مرحله ۶: تأیید نهایی — پلاگین بارگذاری شده؟

وجود پلاگین را بررسی کنید:

```bash
hermes plugins list
```

و وضعیت اتصال:

```bash
hermes gateway status
```

در خروجی باید `bale` به‌صورت `connected` دیده شود.

---

## تأیید (Verification)

برای مطمئن شدن از کارکرد کامل، به ربات بله یک پیام بفرستید و انتظار پاسخ داشته
باشید. همچنین می‌توانید تست خودکار اتصال را اجرا کنید:

```bash
cd ~/.hermes/plugins/platforms/bale
BALE_TEST_CHAT_ID=66881162 python3 tests/test_adapter.py
```

این اسکریپت سه چیز را تست می‌کند: `getMe` (اتصال ربات)، `getUpdates` (دریافت
پیام‌ها) و `sendMessage` (ارسال).

---

## عیب‌یابی

| مشکل | احتمال‌ترین علت | راه‌حل |
|------|------------------|--------|
| `No module named 'telegram'` | پکیج `python-telegram-bot` نصب نیست | `pip install python-telegram-bot` |
| `[Bale] Invalid port: ...` | `base_url` را به‌صورت `/bot` تنظیم نکرده‌اید | مطمئن شوید پلاگین نسخهٔ جدید است (که `https://tapi.bale.ai/bot` را می‌سازد) |
| پلاگین لود نمی‌شود / `not in plugins.enabled` | پلاگین در `plugins.enabled` نیست | آن را به فهرست `plugins.enabled` اضافه کنید |
| ربات پاسخ می‌دهد ولی پیام‌های شما را رد می‌کند | شناسه شما در allowlist نیست | شناسه را به `allow_from` و `BALE_ALLOWED_USERS` اضافه کنید |
| `set_my_commands` خطا می‌دهد | بله هنوز این API را پیاده‌نکرده (Coming soon) | بی‌خطر است؛ فقط یک هشدار است، بقیهٔ کارها درست است |

---

## ارجاع‌ها

- [آموزش راه‌اندازی سریع](tutorial-getting-started.md) — اگر فقط می‌خواهید سریع راه بیفتد
- [راهنمای شخصی‌سازی](howto-customize.md) — محدود کردن دسترسی و تنظیمات پیشرفته
- [مرجع فنی](reference-technical.md) — تمام گزینه‌ها
- [معماری](explanation-architecture.md) — چرا این‌طور ساخته شده