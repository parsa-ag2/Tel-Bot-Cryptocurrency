from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from services.market import (
    get_price,
    get_forex_price,
    get_commodity_price,
    get_usdt_toman,
    find_market,
)


async def market_message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # فقط گروه‌ها
    if update.effective_chat.type == ChatType.PRIVATE:
        return

    if not update.message or not update.message.text:
        return


    text = update.message.text.lower().strip()


    # تشخیص بازار
    market = find_market(text)

    # اگر بازار نبود، هیچ کاری نکن
    if not market:
        return



    # =========================
    # Crypto
    # =========================

    if market["type"] == "crypto":

        coin = market["data"]

        result = get_price(coin["id"])


        if not result:
            return


        usd = result["usd"]
        change = result["change"]


        toman_text = ""

        usdt_toman = get_usdt_toman()

        if usdt_toman:

            toman_text = (
                f"\n🇮🇷 تومان تقریبی:\n"
                f"{usd * usdt_toman:,.0f} تومان"
            )


        await update.message.reply_text(
            f"""
🪙 {coin['name']} ({coin['symbol'].upper()})


💵 قیمت:
${usd:,.2f}


{toman_text}


📊 تغییر 24h:
{change:.2f}%
"""
        )

        return




    # =========================
    # Forex
    # =========================

    elif market["type"] == "forex":

        pair = market["data"]

        result = get_forex_price(pair)


        if not result:
            return


        await update.message.reply_text(
            f"""
💱 {pair}


💵 قیمت:
{result['price']}


📈 تغییر:
{result['change']:.2f}%
"""
        )

        return



    # =========================
    # Commodity
    # =========================

    elif market["type"] == "commodity":

        symbol = market["data"]

        result = get_commodity_price(symbol)


        if not result:
            return


        await update.message.reply_text(
            f"""
📊 {symbol}


💵 قیمت:
{result['price']}


📈 تغییر:
{result['change']:.2f}%
"""
        )

        return