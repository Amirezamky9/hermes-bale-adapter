# Bale Platform Adapter for Hermes Agent

## 📱 خلاصه

این پلاگین امکان ارتباط با Hermes Agent از طریق پیام‌رسان **بله** (Bale) را فراهم می‌کند.

## ✨ ویژگی‌ها

- ✅ پشتیبانی از پیام‌های متنی
- ✅ پشتیبانی از تصاویر، فایل‌ها، ویدیو و صدا
- ✅ پشتیبانی از صفحه کلید inline
- ✅ نشانگر تایپ (typing indicator)
- ✅ پشتیبانی از دستورات (slash commands)
- ✅ قابلیت ارسال پیام‌های cron و notification
- ✅ پشتیبانی از چند کاربر (authorization)

## 🚀 نصب و راه‌اندازی

### ۱. ساخت بازو در بله

1. به [@botfather](https://ble.ir/botfather) در بله پیام بدهید
2. دستور `/newbot` را ارسال کنید
3. نام بازوی خود را وارد کنید
4. توکن دریافتی را ذخیره کنید (فرمت: `123456789:ABC123...`)

### ۲. تنظیم متغیرهای محیطی

فایل `~/.hermes/.env` را ویرایش کنید:

```bash
BALE_BOT_TOKEN=123456789:ABC123...
BALE_ALLOWED_USERS=123456789,987654321  # آیدی کاربران مجاز
BALE_HOME_CHANNEL=123456789  # کانال پیش‌فرض برای cron
```

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
        platform: bale
      typing_indicator: true
```

### ۴. ریستارت گیت‌وی

```bash
hermes gateway restart
```

## 📁 ساختار فایل‌ها

```
~/.hermes/plugins/platforms/bale/
├── plugin.yaml      # متادیتا و تنظیمات
├── __init__.py      # Package init
├── adapter.py       # کلاس اصلی BaleAdapter
├── test_adapter.py  # اسکریپت تست
└── README.md        # این فایل
```

## 🔧 متدهای API بله

### متدهای اصلی

| متد | توضیح |
|-----|--------|
| `getMe` | دریافت اطلاعات بازو |
| `getUpdates` | دریافت آپدیت‌ها (long polling) |
| `sendMessage` | ارسال پیام متنی |
| `sendPhoto` | ارسال تصویر |
| `sendDocument` | ارسال فایل |
| `sendVoice` | ارسال پیام صوتی |
| `sendVideo` | ارسال ویدیو |
| `sendChatAction` | ارسال نشانگر تایپ |

### متدهای اختصاصی بله

| متد | توضیح |
|-----|--------|
| `askReview` | درخواست نظرسنجی |
| `inquireTransaction` | استعلام تراکنش |

## 🔐 امنیت

- **محدودیت کاربران**: فقط کاربران لیست شده در `BALE_ALLOWED_USERS` می‌توانند با بازو تعامل داشته باشند
- **جلوگیری از حلقه**: پیام‌های ارسالی توسط بازو نادیده گرفته می‌شوند
- **اعتبارسنجی**: توکن بازو به صورت امن در `.env` ذخیره می‌شود

## 🐛 عیب‌یابی

### مشکل اتصال

```bash
# تست اتصال
python3 ~/.hermes/plugins/platforms/bale/test_adapter.py
```

### مشکل دریافت پیام

1. مطمئن شوید توکن صحیح است
2. کاربر باید ابتدا به بازو `/start` بزند
3. آیدی کاربر در `BALE_ALLOWED_USERS` باشد

### مشکل ارسال پیام

1. بررسی کنید بازو در گروه عضو است (برای گروه‌ها)
2. مطمئن شوید دسترسی‌های لازم را دارد

## 📚 منابع

- [داکیومنت API بله](https://docs.bale.ai/)
- [داکیومنت همس](https://hermes-agent.nousresearch.com/docs)
- [ساخت بازو در بله](https://ble.ir/botfather)

## 📝 مثال استفادا