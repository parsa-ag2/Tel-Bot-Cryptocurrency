from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ParseMode
from bot.keyboards import chart_keyboard
from services.market import (
    get_price,
    get_forex_price,
    get_commodity_price,
    get_usdt_toman,
    find_market,
    search_coins,
    find_coin_by_name,
)


def now_text():

    return datetime.now().strftime(
        "%Y/%m/%d | %H:%M:%S"
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
    # اول فارکس / کالا / دلار
    # =========================

    market = find_market(text)

    if market:

        pass

    else:

        # =========================
        # بعد کریپتو - بدون لیست، مستقیم بهترین نتیجه
        # =========================

        coin = find_coin_by_name(text)

        if coin:

            market = {
                "type": "crypto",
                "data": coin
            }

        else:

            coins = search_coins(text)

            if coins:

                # به‌جای نمایش لیست، مستقیم بهترین نتیجه رو برمی‌گردونیم
                market = {
                    "type": "crypto",
                    "data": coins[0]
                }

            else:

                market = None

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

        change_emoji = "📈" if change >= 0 else "📉"

        toman_text = ""

        usdt_toman = get_usdt_toman()

        if usdt_toman:

            toman_price = usd * usdt_toman

            toman_text = (
                f"\n🇮🇷 قیمت تقریبی:\n"
                f"<b>{toman_price:,.0f}</b> تومان\n"
            )

        text_reply = (
            f"━━━━━━━━━━━━━━\n"
            f"🪙 <b>{coin['name']} ({coin['symbol'].upper()})</b>\n\n"
            f"💵 قیمت:\n"
            f"<b>${usd:,.2f}</b>\n"
            f"{toman_text}\n"
            f"{change_emoji} تغییر 24h:\n"
            f"<b>{change:.2f}%</b>\n\n"
            f"🕒 بروزرسانی:\n"
            f"{now_text()}\n"
            f"━━━━━━━━━━━━━━\n"
            f"⚡ Live Market"
        )

        await update.message.reply_text(
            text_reply,
            parse_mode=ParseMode.HTML,
            reply_markup=chart_keyboard(
                "crypto",
                coin["id"]
            )
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

        price = result["price"]
        change = result["change"]

        change_emoji = "📈" if change >= 0 else "📉"

        text_reply = (
            f"━━━━━━━━━━━━━━\n"
            f"💱 <b>{pair}</b>\n\n"
            f"💵 قیمت:\n"
            f"<b>{price}</b>\n\n"
            f"{change_emoji} تغییر 24h:\n"
            f"<b>{change:.2f}%</b>\n\n"
            f"🕒 بروزرسانی:\n"
            f"{now_text()}\n"
            f"━━━━━━━━━━━━━━\n"
            f"⚡ Forex Market"
        )

        await update.message.reply_text(
            text_reply,
            parse_mode=ParseMode.HTML,
            reply_markup=chart_keyboard(
                "forex",
                pair
            )
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

        price = result["price"]
        change = result["change"]

        change_emoji = "📈" if change >= 0 else "📉"

        text_reply = (
            f"━━━━━━━━━━━━━━\n"
            f"📊 <b>{symbol}</b>\n\n"
            f"💵 قیمت:\n"
            f"<b>{price}</b>\n\n"
            f"{change_emoji} تغییر 24h:\n"
            f"<b>{change:.2f}%</b>\n\n"
            f"🕒 بروزرسانی:\n"
            f"{now_text()}\n"
            f"━━━━━━━━━━━━━━\n"
            f"⚡ Commodity Market"
        )

        await update.message.reply_text(
            text_reply,
            parse_mode=ParseMode.HTML,
            reply_markup=chart_keyboard(
                "commodity",
                symbol
            )
        )

        return

    # =========================
    # USD / Tether
    # =========================

    elif market["type"] == "usd":

        usdt_toman = get_usdt_toman()

        if not usdt_toman:
            return

        text_reply = (
            f"━━━━━━━━━━━━━━\n"
            f"💵 <b>دلار / تتر (USDT)</b>\n\n"
            f"🇮🇷 قیمت تقریبی:\n"
            f"<b>{usdt_toman:,.0f}</b> تومان\n\n"
            f"🕒 بروزرسانی:\n"
            f"{now_text()}\n"
            f"━━━━━━━━━━━━━━\n"
            f"⚡ Live Market"
        )

        await update.message.reply_text(
            text_reply,
            parse_mode=ParseMode.HTML,
        )

        return