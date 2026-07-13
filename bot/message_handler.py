from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType
from services.market import (
    get_price,
    get_forex_price,
    get_all_forex_pairs,
    get_commodity_price,
    get_usdt_toman,
    search_coins,
    find_coin_by_name,
)



MARKET_WORDS = {

    "دلار": ("usd", "USD"),
    "usd": ("usd", "USD"),

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


    if not update.message or not update.message.text:
        return


    text = update.message.text.lower().strip()


    # =====================
    # 1) Forex
    # =====================

    query = text.upper().replace(" ", "")


    # اگر کاربر جفت ارز نوشته
    if "/" in query:

        result = get_forex_price(query)

        if result:

            await update.message.reply_text(
                f"""
    💱 {query}

    💵 قیمت:
    {result['price']}

    📈 تغییر:
    {result['change']:.2f}%
    """
            )

            return


    # اگر فقط اسم ارز نوشته
    symbol = f"{query}/USD"

    result = get_forex_price(symbol)

    if result:

        await update.message.reply_text(
            f"""
    💱 {symbol}

    💵 قیمت:
    {result['price']}

    📈 تغییر:
    {result['change']:.2f}%
    """
        )

        return


    # =====================
    # 2) USD / Commodities
    # =====================

    for word, data in MARKET_WORDS.items():


        if word in text:


            market_type, symbol = data



            if market_type == "usd":


                usdt_toman = get_usdt_toman()


                if usdt_toman:

                    await update.message.reply_text(
                        f"""
💵 دلار آمریکا


🇮🇷 قیمت:

{usdt_toman:,.0f} تومان
"""
                    )

                return



            elif market_type == "commodity":


                result = get_commodity_price(symbol)


                if result:

                    await update.message.reply_text(
                        f"""
📊 {word}


💵 قیمت:
{result['price']}


📈 تغییر:
{result['change']:.2f}%
"""
                    )

                return




    # =====================
    # 3) Crypto
    # =====================

    query = text.strip()
    normalized_query = query.lower()

    # اول نام کامل را بررسی کن
    coin = find_coin_by_name(normalized_query)

    if not coin:
        coins = search_coins(query)

        if not coins:
            await update.message.reply_text("❌ ارز پیدا نشد.")
            return

        elif len(coins) == 1:
            coin = coins[0]

        else:
            message = "🔍 چند ارز پیدا شد:\n\n"

            for c in coins[:10]:
                message += f"• {c['name']} ({c['symbol'].upper()})\n"

            message += "\nنام کامل ارز را بنویسید."

            await update.message.reply_text(message)
            return
        
    if coin:

        result = get_price(coin["id"])

        if result:

            usd = result["usd"]
            change = result["change"]

            usdt_toman = get_usdt_toman()

            toman_text = ""

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