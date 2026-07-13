from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from services.market import (
    get_price,
    get_forex_price,
    get_commodity_price,
    get_usdt_toman,
    find_market,
    search_coins,
)


async def market_message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # فقط گروه
    if update.effective_chat.type == ChatType.PRIVATE:
        return


    if not update.message or not update.message.text:
        return


    text = update.message.text.lower().strip()


    # جلوگیری از سرچ های الکی
    if len(text) < 2:
        return



    # =========================
    # Crypto Search
    # =========================

    coins = search_coins(text)


    # چند ارز پیدا شد
    if len(coins) > 1:

        message = "🔍 چند ارز پیدا شد:\n\n"


        for i, coin in enumerate(
            coins[:10],
            start=1
        ):

            message += (
                f"{i}️⃣ {coin['name']} "
                f"({coin['symbol'].upper()})\n"
            )


        message += (
            "\nلطفاً نام کامل ارز را وارد کنید."
        )


        await update.message.reply_text(
            message
        )

        return



    # فقط یک ارز پیدا شد
    if len(coins) == 1:

        market = {
            "type": "crypto",
            "data": coins[0]
        }

    else:

        # =========================
        # Forex / Commodity
        # =========================

        market = find_market(text)



    # چیزی پیدا نشد
    if not market:
        return



    # =========================
    # Crypto
    # =========================

    if market["type"] == "crypto":


        coin = market["data"]


        result = get_price(
            coin["id"]
        )


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