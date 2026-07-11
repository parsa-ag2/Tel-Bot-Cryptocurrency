from telegram import ReplyKeyboardMarkup


# =========================
# Main Settings Keyboard
# پنل اصلی تنظیمات
# =========================

def settings_keyboard():

    keyboard = [
        ["👥 مدیریت ادمین‌ها"],
        ["📢 کانال‌های اجباری"],
        ["🔔 تنظیمات هشدار قیمت"],
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================
# Admin Management Keyboard
# مدیریت ادمین ها
# =========================

def admin_keyboard():

    keyboard = [
        ["➕ اضافه کردن ادمین"],
        ["➖ حذف ادمین"],
        ["📋 لیست ادمین‌ها"],
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================
# Channel Management Keyboard
# کانال های اجباری
# =========================

def channel_keyboard():

    keyboard = [
        ["➕ افزودن کانال"],
        ["➖ حذف کانال"],
        ["📋 لیست کانال‌ها"],
        ["🔄 تست اتصال"],
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================
# Price Alert Settings
# هشدار قیمت
# =========================

def alert_keyboard():

    keyboard = [
        ["✅ فعال کردن هشدار"],
        ["❌ غیرفعال کردن هشدار"],
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )