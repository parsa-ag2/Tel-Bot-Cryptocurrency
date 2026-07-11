from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from services.market import (
    get_price,
    get_forex_price,
    get_commodity_price
)

# اسم‌هایی که کاربر ممکنه بنویسه
MARKET_WORDS = {

    # کریپتو
    "btc": ("crypto", "bitcoin"),
    "بیتکوین": ("crypto", "bitcoin"),
    "بیت کوین": ("crypto", "bitcoin"),

    "eth": ("crypto", "ethereum"),
    "اتریوم": ("crypto", "ethereum"),

    "usdt": ("crypto", "tether"),
    "تتر": ("crypto", "tether"),

    "bnb": ("crypto", "binancecoin"),
    "بایننس": ("crypto", "binancecoin"),

    "xrp": ("crypto", "ripple"),
    "ریپل": ("crypto", "ripple"),

    "doge": ("crypto", "dogecoin"),
    "دوج": ("crypto", "dogecoin"),
    "دوج کوین": ("crypto", "dogecoin"),

    "ton": ("crypto", "the-open-network"),
    "تون": ("crypto", "the-open-network"),

    "sol": ("crypto", "solana"),
    "سولانا": ("crypto", "solana"),



    # فارکس
    "eur/usd": ("forex", "EUR/USD"),
    "یورو": ("forex", "EUR/USD"),

    "gbp/usd": ("forex", "GBP/USD"),
    "پوند": ("forex", "GBP/USD"),

    "usd/jpy": ("forex", "USD/JPY"),
    "ین": ("forex", "USD/JPY"),

    "aud/usd": ("forex", "AUD/USD"),
    "دلار استرالیا": ("forex", "AUD/USD"),

    "usd/cad": ("forex", "USD/CAD"),
    "دلار کانادا": ("forex", "USD/CAD"),



    # کالاها
    "طلا": ("commodity", "GOLD"),
    "gold": ("commodity", "GOLD"),

    "نقره": ("commodity", "SILVER"),
    "silver": ("commodity", "SILVER"),

    "نفت برنت": ("commodity", "BRENT"),
    "برنت": ("commodity", "BRENT"),

    "نفت": ("commodity", "WTI"),
    "نفت wti": ("commodity", "WTI"),

    "مس": ("commodity", "COPPER"),
    "گاز": ("commodity", "NATGAS"),
    "گاز طبیعی": ("commodity", "NATGAS"),
}



async def market_message_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):
       
    if update.effective_chat.type == ChatType.PRIVATE:
        return

    text = update.message.text.lower().strip()


    for word, data in MARKET_WORDS.items():

        if word in text.split() or text == word:

            market_type, symbol = data


            # crypto
            if market_type == "crypto":

                result = get_price(symbol)

                if result:

                    await update.message.reply_text(
                        f"""
🪙 {word.upper()}

💵 قیمت:
{result['usd']} $

📊 تغییر 24h:
{result['change']:.2f}%
"""
                    )

            # forex
            elif market_type == "forex":

                result = get_forex_price(symbol)

                if result:

                    await update.message.reply_text(
                        f"""
💱 {symbol}

💵 قیمت:
{result['price']}

📊 تغییر:
{result['change']}%
"""
                    )


            # commodity
            elif market_type == "commodity":

                result = get_commodity_price(symbol)

                if result:

                    await update.message.reply_text(
                        f"""
📊 {word}

💵 قیمت:
{result['price']}

📈 تغییر:
{result['change']}%
"""
                    )


            return