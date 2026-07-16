from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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
def chart_keyboard(
    market_type,
    symbol
):

    keyboard = [

        [
            InlineKeyboardButton(
                "5 دقیقه",
                callback_data=f"chart_{market_type}_{symbol}_5m"
            ),

            InlineKeyboardButton(
                "15 دقیقه",
                callback_data=f"chart_{market_type}_{symbol}_15m"
            ),

        ],

        [
            InlineKeyboardButton(
                "30 دقیقه",
                callback_data=f"chart_{market_type}_{symbol}_30m"
            ),

            InlineKeyboardButton(
                "60 دقیقه",
                callback_data=f"chart_{market_type}_{symbol}_60m"
            ),

        ]
    ]


    return InlineKeyboardMarkup(keyboard)


    return InlineKeyboardMarkup(
        keyboard
    )