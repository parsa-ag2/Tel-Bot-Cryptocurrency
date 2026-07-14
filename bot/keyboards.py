from telegram import ReplyKeyboardMarkup


def home_keyboard():
    keyboard = [
        ["📊 بازارها"],
        ["⚙️ تنظیمات"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def markets_keyboard():
    keyboard = [
        ["🪙 کریپتو"],
        ["💵 فارکس"],
        ["🛢 نفت و کالا"],
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def back_keyboard():
    keyboard = [
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )


def commodities_keyboard():
    keyboard = [
        ["🛢 نفت برنت", "🛢 نفت WTI"],
        ["🟡 طلا", "⚪ نقره"],
        ["🟤 مس", "🔴 گاز طبیعی"],
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )