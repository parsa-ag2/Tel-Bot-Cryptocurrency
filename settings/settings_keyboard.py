from telegram import InlineKeyboardButton, InlineKeyboardMarkup



# =========================
# Main Settings Keyboard
# پنل اصلی تنظیمات
# =========================

def settings_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "👥 مدیریت ادمین‌ها",
                callback_data="admin_panel"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 کانال‌های اجباری",
                callback_data="channel_panel"
            )
        ],

        [
            InlineKeyboardButton(
                "🔔 تنظیمات هشدار قیمت",
                callback_data="alert_settings"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="back"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# Admin Management Keyboard
# مدیریت ادمین ها
# =========================

def admin_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "➕ اضافه کردن ادمین",
                callback_data="add_admin"
            )
        ],

        [
            InlineKeyboardButton(
                "➖ حذف ادمین",
                callback_data="remove_admin"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 لیست ادمین‌ها",
                callback_data="list_admins"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="settings"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# Channel Management Keyboard
# کانال های اجباری
# =========================

def channel_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "➕ افزودن کانال",
                callback_data="add_channel"
            )
        ],

        [
            InlineKeyboardButton(
                "➖ حذف کانال",
                callback_data="remove_channel"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 لیست کانال‌ها",
                callback_data="list_channels"
            )
        ],

        [
            InlineKeyboardButton(
                "🔄 تست اتصال",
                callback_data="test_channel"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="settings"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )



# =========================
# Price Alert Settings
# هشدار قیمت
# =========================

def alert_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "✅ فعال کردن هشدار",
                callback_data="enable_alert"
            )
        ],

        [
            InlineKeyboardButton(
                "❌ غیرفعال کردن هشدار",
                callback_data="disable_alert"
            )
        ],

        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="settings"
            )
        ]

    ]


    return InlineKeyboardMarkup(
        keyboard
    )