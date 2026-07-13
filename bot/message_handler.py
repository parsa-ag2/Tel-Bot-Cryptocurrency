from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from services.market import (
    get_price,
    get_forex_price,
    get_all_forex_pairs,
    get_commodity_price,
    get_usdt_toman,
    find_coin,
)


MARKET_WORDS = {

    # دلار
    "دلار": ("usd", "USD"),
    "usd": ("usd", "USD"),


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

    # فقط گروه
    if update.effective_chat.type == ChatType.PRIVATE:
        return


    if not update.message or not update.message.text:
        return


    text = update.message.text.lower().strip()



    # =====================
    # Crypto
    # =====================

    coin = find_coin(text)

    if coin:

        result = get_price(
            coin["id"]
        )


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




    # =====================
    # Dynamic Forex
    # =====================

    forex_pairs = get_all_forex_pairs()


    query = text.upper().replace(
        " ",
        ""
    )


    for pair in forex_pairs:

        normalized = pair.replace(
            "/",
            ""
        )


        if query == normalized:


            result = get_forex_price(
                pair
            )


            if result:

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




    # =====================
    # USD / Commodities
    # =====================

    for word, data in MARKET_WORDS.items():


        if word in text:


            market_type, symbol = data



            # -----------------
            # دلار
            # -----------------

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




            # -----------------
            # Commodity
            # -----------------

            elif market_type == "commodity":


                result = get_commodity_price(
                    symbol
                )


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