from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.membership import check_user_membership
from telegram.constants import ChatType
from datetime import datetime
from services.chart import create_chart
from services.market import (
    get_price,
    get_forex_price,
    get_all_forex_pairs,
    get_commodity_price,
    get_usdt_toman,
    search_coins,
    find_coin_by_name,
    find_market
)
from bot.keyboards import (
    home_keyboard,
    markets_keyboard,
    commodities_keyboard,
    chart_keyboard,
    timeframe_keyboard
)



COMMODITIES = {
    "🛢 نفت برنت": ("BRENT", "🛢"),
    "🛢 نفت WTI": ("WTI", "🛢"),
    "🟡 طلا": ("GOLD", "🟡"),
    "⚪ نقره": ("SILVER", "⚪"),
    "🟤 مس": ("COPPER", "🟤"),
    "🔴 گاز طبیعی": ("NATGAS", "🔴"),
}

async def send_price(update: Update, coin: dict):

    loading = await update.message.reply_text(
        "📡 دریافت قیمت بازار 🔄"
    )


    data = get_price(coin["id"])

    if not data:

        await loading.edit_text(
            "❌ خطا در دریافت قیمت."
        )

        return


    usd = data["usd"]
    change = data["change"]


    usdt_toman = get_usdt_toman()


    toman_text = ""

    if usdt_toman:

        toman_price = usd * usdt_toman

        toman_text = (
            f"\n🇮🇷 قیمت تقریبی:\n"
            f"<b>{toman_price:,.0f}</b> تومان\n"
        )


    change_emoji = "📈" if change >= 0 else "📉"


    now = datetime.now().strftime(
        "%Y/%m/%d | %H:%M:%S"
    )


    text = (

        f"━━━━━━━━━━━━━━\n"
        f"🪙 <b>{coin['name']} ({coin['symbol'].upper()})</b>\n\n"

        f"💵 قیمت:\n"
        f"<b>${usd:,.2f}</b>\n"

        f"{toman_text}\n"

        f"{change_emoji} تغییر 24h:\n"
        f"<b>{change:.2f}%</b>\n\n"

        f"🕒 بروزرسانی:\n"
        f"{now}\n"

        f"━━━━━━━━━━━━━━\n"
        f"⚡ Live Market"

    )


    await loading.edit_text(
    text,
    parse_mode=ParseMode.HTML,
    reply_markup=chart_keyboard(
        "crypto",
        coin["id"]
    )
)





async def send_forex(update: Update, pair: str):

    loading = await update.message.reply_text(
        "📡 دریافت اطلاعات فارکس 🔄"
    )


    data = get_forex_price(pair)


    if not data:

        await loading.edit_text(
            "❌ خطا در دریافت قیمت."
        )

        return



    price = data["price"]
    change = data["change"]



    change_emoji = "📈" if change >= 0 else "📉"



    now = datetime.now().strftime(
        "%Y/%m/%d | %H:%M:%S"
    )


    text = (

        f"━━━━━━━━━━━━━━\n"
        f"💱 <b>{pair}</b>\n\n"

        f"💵 قیمت:\n"
        f"<b>{price}</b>\n\n"

        f"{change_emoji} تغییر 24h:\n"
        f"<b>{change:.2f}%</b>\n\n"

        f"🕒 بروزرسانی:\n"
        f"{now}\n"

        f"━━━━━━━━━━━━━━\n"
        f"⚡ Forex Market"

    )


    await loading.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=chart_keyboard(
            "forex",
            pair
        )
    )







async def send_commodity(update, symbol):

    loading = await update.message.reply_text(
        "📡 دریافت اطلاعات بازار 🔄"
    )


    code, emoji = COMMODITIES[symbol]


    data = get_commodity_price(code)


    if not data:

        await loading.edit_text(
            "❌ خطا در دریافت قیمت."
        )

        return



    price = data["price"]
    change = data["change"]



    



    now = datetime.now().strftime(
        "%Y/%m/%d | %H:%M:%S"
    )



    text = (

        f"━━━━━━━━━━━━━━\n"
        f"{emoji} <b>{symbol}</b>\n\n"

        f"💵 قیمت:\n"
        f"<b>{price}</b>\n\n"

        f"🕒 بروزرسانی:\n"
        f"{now}\n"

        f"━━━━━━━━━━━━━━\n"
        f"⚡ Commodity Market"

    )



    await loading.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=chart_keyboard(
            "commodity",
            code
        )
    )

async def chart_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    # فقط گروه
    if query.message.chat.type == "private":
        return


    data = query.data
    # =========================
# باز کردن منوی چارت
# =========================

    if data.startswith("chartmenu_"):

        _, market_type, symbol = data.split("_")


        await query.message.reply_text(
            "⏱ تایم‌فریم را انتخاب کنید:",
            reply_markup=timeframe_keyboard(
                market_type,
                symbol
            )
        )

        return


    try:

        # chart_crypto_bitcoin_15m
        # chart_forex_EUR/USD_15m
        # chart_commodity_GOLD_15m

        _, market_type, symbol, timeframe = data.split("_")


    except ValueError:

        await query.message.reply_text(
            "❌ اطلاعات چارت اشتباه است."
        )

        return



    loading = await query.message.reply_text(
        "📊 در حال ساخت چارت 🔄"
    )



    try:

        file = create_chart(
            market_type,
            symbol,
            timeframe
        )


        await loading.delete()


        await query.message.reply_photo(
            photo=open(
                file,
                "rb"
            ),
            caption=(
                f"📈 چارت {symbol}\n"
                f"⏱ تایم‌فریم: {timeframe}"
            )
        )


    except Exception as e:

        print(
            "CHART ERROR:",
            e
        )


        await loading.edit_text(
            "❌ خطا در ساخت چارت."
        )




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    allowed = await check_user_membership(
        update,
        context
    )

    if not allowed:
        return
    
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

    allowed = await check_user_membership(
        update,
        context
    )

    if not allowed:
        return


    if update.effective_chat.type != ChatType.PRIVATE:
        return


    text = update.message.text.strip()

    # =========================
    # دکمه ها
    # =========================

    if text == "📊 بازارها":

        await update.message.reply_text(
            "نوع بازار را انتخاب کن 👇",
            reply_markup=markets_keyboard()
        )
        return


    elif text == "🪙 کریپتو":

        context.user_data.clear()
        context.user_data["waiting_crypto"] = True

        await update.message.reply_text(
            "🪙 نام یا نماد ارز را وارد کنید.\n\n"
            "مثال:\n"
            "BTC\n"
            "ETH\n"
            "Bitcoin"
        )
        return


    elif text == "💵 فارکس":

        context.user_data.clear()
        context.user_data["waiting_forex"] = True

        await update.message.reply_text(
            "💱 نماد فارکس را وارد کنید.\n\n"
            "مثال:\n"
            "EUR\n"
            "EUR/USD\n"
            "USD/JPY"
        )
        return


    elif text == "🛢 نفت و کالا":

        context.user_data.clear()
        context.user_data["waiting_commodity"] = True

        await update.message.reply_text(
            "کالای موردنظر را انتخاب کن 👇",
            reply_markup=commodities_keyboard()
        )
        return


    elif text == "🔙 بازگشت":

        context.user_data.clear()

        await update.message.reply_text(
            "منوی اصلی",
            reply_markup=home_keyboard()
        )
        return

    # =========================
    # حالت کریپتو
    # =========================

    if context.user_data.get("waiting_crypto"):

        query = text.strip()

        coin = find_coin_by_name(
            query.lower()
        )

        if coin:

            await send_price(
                update,
                coin
            )

            return


        coins = search_coins(query)


        if not coins:

            await update.message.reply_text(
                "❌ ارز پیدا نشد.\n"
                "نام یا نماد ارز را درست وارد کنید."
            )

            return



        if len(coins) == 1:

            await send_price(
                update,
                coins[0]
            )

            return



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



    # =========================
    # حالت فارکس
    # =========================

    if context.user_data.get("waiting_forex"):


        query = text.upper().replace(
            " ",
            ""
        )


        pairs = get_all_forex_pairs()



        # EUR/USD

        if query in pairs:

            await send_forex(
                update,
                query
            )

            return



        # EUR تبدیل شود به EUR/USD

        pair = query + "/USD"


        if pair in pairs:

            await send_forex(
                update,
                pair
            )

            return



        await update.message.reply_text(
            "❌ جفت ارز پیدا نشد."
        )

        return




    # =========================
    # حالت کالاها
    # =========================

    if context.user_data.get("waiting_commodity"):


        if text in COMMODITIES:

            await send_commodity(
                update,
                text
            )

            return



        await update.message.reply_text(
            "❌ کالا پیدا نشد."
        )

        return




    # =========================
    # حالت عادی منو
    # =========================


    market = find_market(
        text.lower()
    )


    if market:


        if market["type"] == "crypto":

            await send_price(
                update,
                market["data"]
            )

            return



        elif market["type"] == "forex":

            await send_forex(
                update,
                market["data"]
            )

            return



        elif market["type"] == "commodity":

            await send_commodity(
                update,
                market["data"]
            )

            return




    else:
        return