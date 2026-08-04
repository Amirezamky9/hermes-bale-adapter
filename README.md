# Bale Platform Adapter for Hermes Agent

## 📱 خلاصه

این پلاگین امکان ارتباط با Hermes Agent از طریق پیام‌رسان **بله** (Bale) را فراهم می‌کند.

> 🧠 **این پلاگین یک کپی فنی از پلاگین تلگرام است** که فقط تغییرات لازم برای بله را دریافت کرده — چون API بله تقریباً ۹۰٪ با تلگرام سازگار است. جزئیات در [معماری](docs/explanation-architecture.md).

## ✨ ویژگی‌ها

- ✅ پشتیبانی از پیام‌های متنی
- ✅ پشتیبانی از تصاویر، فایل‌ها، ویدیو و صدا
- ✅ پشتیبانی از صفحه‌کلید inline
- ✅ نشانگر تایپ (typing indicator)
- ✅ پشتیبانی از دستورات (slash commands)
- ✅ قابلیت ارسال پیام‌های cron و notification
- ✅ پشتیبانی از چند کاربر (authorization)

## 🚀 نصب و راه‌اندازی

### ۱. ساخت ربات در بله

1. به [@botfather](https://ble.ir/botfather) در بله پیام بدهید
2. دستور `/newbot` را ارسال کنید
3. نام ربات خود را وارد کنید
4. توکن دریافتی را ذخیره کنید (فرمت: `123456789:ABC123...`)

### ۲. تنظیم متغیرهای محیطی

از روی نمونه، فایل `.env` را در پوشهٔ پلاگین بسازید:

```bash
cd ~/.hermes/plugins/platforms/bale
cp .env.example .env
```

سپس `.env` را ویرایش کنید:

```bash
BALE_BOT_TOKEN=123456789:ABC123...
BALE_ALLOWED_USERS=123456789,987654321  # آیدی کاربران مجاز
BALE_HOME_CHANNEL=123456789             # کانال پیش‌فرض برای cron
BALE_ALLOW_ALL_USERS=0                  # 1 = اجازه به همه (فقط توسعه)
```

> 📌 `.env` در `~/.hermes/.env` هم خوانده می‌شود؛ مطمئن شوید توکن در همان جایی که هرمس اجرا می‌شود در دسترس است.

### ۳. اضافه کردن به config.yaml

فایل `~/.hermes/config.yaml` را ویرایش کنید:

```yaml
gateway:
  platforms:
    bale:
      enabled: true
      token: 123456789:ABC123...
      extra:
        allow_from:
          - '123456789'
      home_channel:
        chat_id: '123456789'
        name: YourName
      typing_indicator: true
```

**و مهم‌تر:** پلاگین را در `plugins.enabled` فعال کنید — بدون این، پلاگین لود نمی‌شود:

```yaml
plugins:
  enabled:
    - platforms/bale
```

> ⚠️ **نکتهٔ مهم:** اگر یک بلوک تکراری `bale` در سطح بالای `platforms:` دارید (خارج از `gateway.`)، مقدار `enabled` آن **روی** تنظیمات gateway می‌نشیند. هر دو را `true` نگه دارید، وگرنه پلاگین با وجود `enabled: true` کار نمی‌کند.

### ۴. ری‌استارت گیت‌وی

```bash
hermes gateway restart
```

وضعیت اتصال را چک کنید:

```bash
hermes gateway status   # باید bale: connected باشد
```

### ۵. تست اتصال

```bash
cd ~/.hermes/plugins/platforms/bale
BALE_TEST_CHAT_ID=123456789 python3 tests/test_adapter.py
```

> این اسکریپت سه چیز را تست می‌کند: `getMe` (اتصال)، `getUpdates` (دریافت) و `sendMessage` (ارسال).

## 📚 مستندات

برای یک راهنمای کامل و ساختاریافته (آموزش، نصب، شخصی‌سازی، مرجع، معماری) این بخش‌ها را بخوانید:

| بخش | شرح |
|-----|------|
| [ایندکس مستندات](docs/README.md) | راهنمای انتخاب بخش مناسب |
| [آموزش راه‌اندازی سریع](docs/tutorial-getting-started.md) | از صفر تا اولین پیام در ۵ گام |
| [راهنمای نصب کامل](docs/howto-install.md) | نصب گام‌به‌گام روی هر سیستم‌عامل |
| [راهنمای شخصی‌سازی](docs/howto-customize.md) | محدود کردن دسترسی و تنظیمات پیشرفته |
| [مرجع فنی](docs/reference-technical.md) | تمام گزینه‌ها و متغیرهای محیطی |
| [معماری: چرا کپی از تلگرام؟](docs/explanation-architecture.md) | چرا و چگونه این پلاگین ساخته شد |

## 📁 ساختار فایل‌ها

```
~/.hermes/plugins/platforms/bale/
├── plugin.yaml      # متادیتا و تنظیمات
├── __init__.py      # Package init
├── adapter.py       # کلاس اصلی BaleAdapter
├── bale_ids.py      # نرمال‌سازی شناسه چت
├── bale_network.py  # ترابرد شبکهٔ جایگزین
├── tests/           # تست‌های اتصال (test_adapter.py)
├── docs/            # مستندات (همین مجموعه)
├── .env.example     # نمونهٔ متغیرهای محیطی
├── .gitignore       # فایل‌های حساس را از git دور نگه می‌دارد
├── LICENSE          # مجوز MIT
└── README.md        # این فایل
```

## 🔧 متدهای API بله

| متد | توضیح |
|-----|--------|
| `getMe` | دریافت اطلاعات ربات |
| `getUpdates` | دریافت آپدیت‌ها (long polling) |
| `sendMessage` | ارسال پیام متنی |
| `sendPhoto` | ارسال تصویر |
| `sendDocument` | ارسال فایل |
| `sendVoice` | ارسال پیام صوتی |
| `sendVideo` | ارسال ویدیو |
| `sendChatAction` | ارسال نشانگر تایپ |

## 🔐 امنیت

- **محدودیت کاربران**: فقط کاربران لیست‌شده در `allow_from` / `BALE_ALLOWED_USERS` می‌توانند با ربات تعامل داشته باشند
- **جلوگیری از حلقه**: پیام‌های ارسال‌شده توسط خود ربات نادیده گرفته می‌شوند
- **اعتبارسنجی**: توکن ربات به‌صورت امن در `.env` ذخیره می‌شود (و در `.gitignore` است)

## 🐛 عیب‌یابی

### مشکل اتصال

```bash
# تست اتصال
cd ~/.hermes/plugins/platforms/bale
BALE_TEST_CHAT_ID=123456789 python3 tests/test_adapter.py
```

### خطای `[Bale] Invalid port: ...`

- **علت:** `base_url` بدون پسوند `/bot` ساخته شده است. آدرس درست: `https://tapi.bale.ai/bot<TOKEN>/<METHOD>`.
- **راه‌حل:** مطمئن شوید پلاگین نسخهٔ جدید است (که `https://tapi.bale.ai/bot` را به‌عنوان پایه می‌سازد).

### هشدار `set_my_commands` → `Not Implemented`

- **بی‌خطر است.** بله هنوز این endpoint را پیاده‌نکرده؛ فقط یک هشدار است و بقیهٔ کارها درست کار می‌کند.

### مشکل دریافت پیام

1. مطمئن شوید توکن صحیح است
2. کاربر باید ابتدا به ربات `/start` بزند
3. آیدی کاربر در `allow_from` / `BALE_ALLOWED_USERS` باشد

### مشکل ارسال پیام

1. بررسی کنید ربات در گروه عضو است (برای گروه‌ها)
2. مطمئن شوید دسترسی‌های لازم را دارد

## 📚 منابع

- [داکیومنت API بله](https://docs.bale.ai/)
- [داکیومنت هرمس](https://hermes-agent.nousresearch.com/docs)
- [ساخت ربات در بله](https://ble.ir/botfather)

## 📝 مثال استفاده

ارسال یک پیام مستقیم به چت (با توکن ربات):

```bash
curl -X POST "https://tapi.bale.ai/bot<TOKEN>/sendMessage" \
  -d chat_id=123456789 \
  -d text="سلام! این یک تست است."
```
