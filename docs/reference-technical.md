# مرجع فنی پلاگین بله

این صفحه، مرجع کامل و دقیق پلاگین است: ساختار فایل‌ها، متغیرهای محیطی، گزینه‌های
پیکربندی، و سطح API. هر ادعا مستقیماً از کد استخراج شده است.

---

## نمای کلی

پلاگین `bale-platform` یک آداپتور پیام‌رسان برای Hermes Agent است. از کتابخانهٔ
`python-telegram-bot` (نسخه سازگار با Bot API بله) استفاده می‌کند و با تغییر
`base_url` به `https://tapi.bale.ai` با بله ارتباط برقرار می‌کند.

- **نوع:** `platform`
- **نام پلاگین:** `bale-platform`
- **کلاس اصلی:** `BaleAdapter` (زیرکلاس `BasePlatformAdapter`)
- **شناسه پلتفرم:** `Platform("bale")` — در رجیستری به‌صورت `Platform.BALE` ثبت می‌شود
- **کتابخانه اصلی:** `python-telegram-bot`
- **نقطه اتصال:** `https://tapi.bale.ai/bot<TOKEN>/<METHOD>` (و `https://tapi.bale.ai/file/bot<TOKEN>/<FILE_PATH>` برای فایل‌ها)

---

## ساختار فایل‌ها

```
hermes-bale-adapter/
├── __init__.py          # خروجی register از adapter
├── adapter.py           # کلاس اصلی BaleAdapter (8,256 خط)
├── bale_ids.py          # نرمال‌سازی شناسه چت‌ها
├── bale_network.py      # ترابرد شبکهٔ جایگزین (failover با IP مستقیم)
├── plugin.yaml          # متادیتای پلاگین (نام، وابستگی‌ها، متغیرهای محیطی)
├── .env.example         # نمونهٔ متغیرهای محیطی
├── .gitignore           # فایل‌های حساس را از git دور نگه می‌دارد
├── LICENSE              # مجوز MIT
├── README.md            # معرفی پروژه
├── docs/                # مستندات (همین مجموعه)
└── tests/
    └── test_adapter.py  # تست‌های اتصال: getMe / getUpdates / sendMessage
```

---

## متغیرهای محیطی

### الزامی

| متغیر | شرح | فرمت |
|--------|------|------|
| `BALE_BOT_TOKEN` | توکن ربات از @botfather | `123456789:ABCdef...` |

### اختیاری — دسترسی

| متغیر | پیش‌فرض | شرح |
|--------|---------|------|
| `BALE_ALLOWED_USERS` | خالی (همه مجاز) | لیست شناسه‌های مجاز، با کاما جدا شده |
| `BALE_ALLOW_ALL_USERS` | `0` | `1` = همه می‌توانند (فقط تست) |

### اختیاری — مقصد اعلان‌ها

| متغیر | پیش‌فرض | شرح |
|--------|---------|------|
| `BALE_HOME_CHANNEL` | خالی | شناسه چت پیش‌فرض برای cron/notification |
| `BALE_HOME_CHANNEL_NAME` | خالی | نام نمایشی چت خانگی |

### اختیاری — رفتار پیام‌رسانی

| متغیر | پیش‌فرض | شرح |
|--------|---------|------|
| `HERMES_BALE_TEXT_BATCH_DELAY_SECONDS` | مقدار هرمس | تأخیر بین دسته‌های متن |
| `HERMES_BALE_TEXT_BATCH_SPLIT_DELAY_SECONDS` | مقدار هرمس | تأخیر بین پیام‌های جدا |
| `HERMES_BALE_MEDIA_BATCH_DELAY_SECONDS` | `0.8` | تأخیر بین ارسال‌های رسانه |

---

## پیکربندی در config.yaml

### ساختار کامل

```yaml
gateway:
  platforms:
    bale:
      enabled: true                    # فعال بودن پلاگین
      token: 123456789:ABCdef...       # توکن ربات
      base_url: https://tapi.bale.ai/bot   # اختیاری — نقطه اتصال (پیش‌فرض همین)
      base_file_url: https://tapi.bale.ai/file/bot  # اختیاری — نقطه فایل
      extra:
        allow_from:                    # اختیاری — لیست شناسه‌های مجاز
          - '66881162'
        typing_indicator: true         # اختیاری — نشانگر «در حال نوشتن…»
      home_channel:                    # اختیاری — مقصد اعلان‌ها
        chat_id: '66881162'
        name: پیام شخصی
```

### نکتهٔ مهم دربارهٔ `plugins.enabled`

پلاگین باید در `plugins.enabled` هم باشد:

```yaml
plugins:
  enabled:
    - platforms/bale
```

> ⚠️ اگر بلوک تکراری `bale` در سطح `platforms:` دارید (خارج از `gateway.`)، مقدار
> `enabled` آن **روی** مقدار `gateway.platforms.bale.enabled` می‌نشیند. هر دو را
> `true` نگه دارید. (این دقیقاً همان باگی بود که در توسعهٔ این پلاگین کشف و رفع شد.)

---

## سطح API (Public Surface)

### کلاس‌ها

| کلاس | نقش |
|-------|------|
| `BaleAdapter` | آداپتور اصلی؛ ارسال/دریافت/استریم/دکمه‌ها |
| `BaleFallbackTransport` | ترابرد جایگزین (در `bale_network.py`) — failover با IP مستقیم وقتی `tapi.bale.ai` دچار مشکل DNS/شبکه می‌شود |

### توابع کمکی (در `bale_ids.py`)

| تابع | شرح |
|-------|------|
| `normalize_bale_chat_id(value)` | شناسه چت را به رشتهٔ استاندارد تبدیل می‌کند (برای مقایسهٔ مطمئن در دیتابیس) |

### کلاس‌های خارجی استفاده‌شده (از python-telegram-bot)

| کلاس | کاربرد |
|-------|--------|
| `Application` | مدیریت polling و دریافت آپدیت‌ها |
| `Bot` | ارسال پیام‌ها و فراخوانی API |
| `Message` / `Update` | نمایش پیام‌ها و آپدیت‌ها |
| `InlineKeyboardButton` / `InlineKeyboardMarkup` | دکمه‌های تعاملی (پیکر مدل و غیره) |
| `CommandHandler` / `CallbackQueryHandler` / `MessageHandler` | مسیریابی دستورها و پاسخ‌های دکمه‌ها |
| `ParseMode` | حالت‌های رندر: `MARKDOWN` و `HTML` (نه `MARKDOWN_V2`) |

---

## رفتارهای خاص بله

### ۱. حالت‌های رندر (Parse Mode)

بله از `Markdown` و `HTML` پشتیبانی می‌کند، اما **نه** `MarkdownV2`. این پلاگین:

- از `ParseMode.MARKDOWN` استفاده می‌کند (نه `MARKDOWN_V2`)
- جدول‌ها را به بولت‌لیست تبدیل می‌کند (چون بله جدول markdown را پشتیبانی نمی‌کند)
- کاراکترهای escape خاص MarkdownV2 را اعمال نمی‌کند

### ۲. صفحه‌کلید inline و RTL

پیکر مدل (`/model`) کاملاً فارسی و راست‌به‌چپ است:

- دکمه‌ها: «بعدی»، «قبلی»، «بازگشت»، «انصراف»
- «بعدی» سمت راست، «قبلی» سمت چپ (سازگار با RTL بله)
- نام مدل‌های بلند (مثل `nvidia/nemotron-3-ultra-550b-a55b:free`) کوتاه و بدون
  پسوند `:free` نمایش داده می‌شوند تا در دکمه جا شوند

### ۳. ترابرد شبکهٔ جایگزین

`bale_network.py` یک `BaleFallbackTransport` ارائه می‌دهد که وقتی اتصال مستقیم به
`tapi.bale.ai` قطع می‌شود، از IP مستقیم استفاده می‌کند (failover) تا ربات در
شرایط بد شبکه هم پاسخگو بماند.

---

## عیب‌یابی (مرجع)

| کد خطا | معنی | راه‌حل |
|---------|------|--------|
| `Invalid port: '<token-part>'` | URL به‌صورت `host:token` ساخته شده (بدون `/bot`) | پلاگین جدید که `base_url` را با `/bot` می‌سازد نصب کنید |
| `set_my_commands` → `Not Implemented` | بله این endpoint را هنوز ندارد | بی‌خطر؛ فقط یک هشدار است |
| `[Bale]` در لاگ نیست | پلاگین لود نشده | چک `plugins.enabled` و `enabled: true` در هر دو بلوک |

---

## ارجاع‌ها

- [آموزش راه‌اندازی سریع](tutorial-getting-started.md)
- [راهنمای نصب](howto-install.md)
- [راهنمای شخصی‌سازی](howto-customize.md)
- [معماری](explanation-architecture.md)