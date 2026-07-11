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
        ["🔙 بازگشت"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )



def crypto_keyboard():

    keyboard = [
        ["🟠 BTC", "🔵 ETH"],
        ["🟢 USDT", "🟡 BNB"],
        ["⚪ XRP", "🟤 DOGE"],
        ["🔷 TON", "🟣 SOL"],
        ["🔙 بازگشت"],
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )

def forex_keyboard():

    keyboard = [
        ["🇪🇺 EUR/USD", "🇬🇧 GBP/USD"],
        ["🇺🇸 USD/JPY", "🇦🇺 AUD/USD"],
        ["🇺🇸 USD/CAD", "🇳🇿 NZD/USD"],
        ["🇪🇺 EUR/JPY", "🇬🇧 GBP/JPY"],
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