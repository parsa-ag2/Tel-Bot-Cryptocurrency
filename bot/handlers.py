from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from services.market import get_price, get_forex_price,get_commodity_price
from bot.keyboards import (
    home_keyboard,
    markets_keyboard,
    crypto_keyboard,
    forex_keyboard,
    commodities_keyboard
)




COINS = {
    "bitcoin": ("بیت‌کوین (BTC)", "🟠"),
    "ethereum": ("اتریوم (ETH)", "🔵"),
    "tether": ("تتر (USDT)", "🟢"),
    "binancecoin": ("بایننس‌کوین (BNB)", "🟡"),
    "ripple": ("ریپل (XRP)", "⚪"),
    "dogecoin": ("دوج‌کوین (DOGE)", "🟤"),
    "toncoin": ("تون‌کوین (TON)", "🔷"),
    "solana": ("سولانا (SOL)", "🟣"),
}

CRYPTO_BUTTONS = {
    "🟠 BTC": "bitcoin",
    "🔵 ETH": "ethereum",
    "🟢 USDT": "tether",
    "🟡 BNB": "binancecoin",
    "⚪ XRP": "ripple",
    "🟤 DOGE": "dogecoin",
    "🔷 TON": "toncoin",
    "🟣 SOL": "solana",
}

FOREX = {
    "EUR/USD": ("یورو / دلار", "🇪🇺"),
    "GBP/USD": ("پوند / دلار", "🇬🇧"),
    "USD/JPY": ("دلار / ین", "🇯🇵"),
    "AUD/USD": ("دلار استرالیا / دلار", "🇦🇺"),
    "USD/CAD": ("دلار / دلار کانادا", "🇨🇦"),
    "NZD/USD": ("دلار نیوزیلند / دلار", "🇳🇿"),
    "EUR/JPY": ("یورو / ین", "🇪🇺"),
    "GBP/JPY": ("پوند / ین", "🇬🇧"),
}


FOREX_BUTTONS = {
    "🇪🇺 EUR/USD": "EUR/USD",
    "🇬🇧 GBP/USD": "GBP/USD",
    "🇯🇵 USD/JPY": "USD/JPY",
    "🇦🇺 AUD/USD": "AUD/USD",
    "🇨🇦 USD/CAD": "USD/CAD",
    "🇳🇿 NZD/USD": "NZD/USD",
    "🇪🇺 EUR/JPY": "EUR/JPY",
    "🇬🇧 GBP/JPY": "GBP/JPY",
}

COMMODITIES = {
    "🛢 نفت برنت": ("BRENT", "🛢"),
    "🛢 نفت WTI": ("WTI", "🛢"),
    "🟡 طلا": ("GOLD", "🟡"),
    "⚪ نقره": ("SILVER", "⚪"),
    "🟤 مس": ("COPPER", "🟤"),
    "🔴 گاز طبیعی": ("NATGAS", "🔴"),
}

async def send_price(update: Update, coin_id: str):

    name, emoji = COINS[coin_id]

    data = get_price(coin_id)

    if not data:
        await update.message.reply_text("❌ خطا در دریافت قیمت.")
        return

    usd = data["usd"]
    change = data["change"]

    change_emoji = "📈" if change >= 0 else "📉"

    text = (
        f"{emoji} <b>{name}</b>\n\n"
        f"💵 قیمت: <b>${usd:,.2f}</b>\n"
        f"{change_emoji} تغییر ۲۴ ساعته: <b>{change:.2f}%</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
    )


async def send_forex(update: Update, pair: str):

    name, emoji = FOREX[pair]

    data = get_forex_price(pair)

    if not data:
        await update.message.reply_text("❌ خطا در دریافت قیمت.")
        return

    price = data["price"]
    change = data["change"]

    change_emoji = "📈" if change >= 0 else "📉"

    text = (
        f"{emoji} <b>{name}</b>\n\n"
        f"💵 قیمت: <b>{price}</b>\n"
        f"{change_emoji} تغییر: <b>{change:.2f}%</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
    )


async def send_commodity(update, symbol):

    code, emoji = COMMODITIES[symbol]

    data = get_commodity_price(code)

    if not data:
        await update.message.reply_text("❌ خطا در دریافت قیمت")
        return

    text = (
        f"{emoji} <b>{symbol}</b>\n\n"
        f"💲 قیمت: <b>{data['price']}</b>\n"
        f"📈 تغییر: <b>{data['change']:.2f}%</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.type != ChatType.PRIVATE:

        await update.message.reply_text(
            "👋 برای استفاده از منوها، در چت خصوصی به من پیام بده."
        )
        return

    await update.message.reply_text(
        "سلام 👋 به ربات خوش اومدی!",
        reply_markup=home_keyboard(),
    )


async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_chat.type != ChatType.PRIVATE:
        return


    text = update.message.text


    if text == "📊 بازارها":

        await update.message.reply_text(
            "نوع بازار را انتخاب کن 👇",
            reply_markup=markets_keyboard(),
        )


    elif text == "🪙 کریپتو":

        await update.message.reply_text(
            "ارز مورد نظر را انتخاب کن 👇",
            reply_markup=crypto_keyboard(),
        )


    elif text == "💵 فارکس":

        await update.message.reply_text(
            "جفت ارز موردنظر را انتخاب کن 👇",
            reply_markup=forex_keyboard(),
        )


    elif text == "🛢 نفت و کالا":

        await update.message.reply_text(
            "کالای موردنظر را انتخاب کن 👇",
            reply_markup=commodities_keyboard()
        )


    elif text == "🔙 بازگشت":

        await update.message.reply_text(
            "منوی اصلی",
            reply_markup=home_keyboard(),
        )

    elif text == "🔙 بازگشت":

        await update.message.reply_text(
            "منوی اصلی",
            reply_markup=home_keyboard(),
        )

    elif text in CRYPTO_BUTTONS:

        await send_price(update, CRYPTO_BUTTONS[text])

    elif text in FOREX_BUTTONS:

        await send_forex(update, FOREX_BUTTONS[text])

    elif text in COMMODITIES:

        await send_commodity(update, text)

    else:
        return

