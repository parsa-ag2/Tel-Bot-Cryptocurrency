from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)


def app_keyboard():

    keyboard = [
        [
            KeyboardButton(
                "📱 باز کردن منو",
                web_app=WebAppInfo(
                    url="https://YOUR_DOMAIN.com"
                )
            )
        ]
    ]


    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )