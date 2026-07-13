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


def forex_keyboard(pairs):

    keyboard = []

    row = []

    for pair in pairs:

        row.append(
            f"💱 {pair}"
        )

        # هر ردیف 2 دکمه
        if len(row) == 2:
            keyboard.append(row)
            row = []


    # اگر یکی باقی ماند
    if row:
        keyboard.append(row)


    keyboard.append(
        ["🔙 بازگشت"]
    )


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