from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from bot.membership import check_user_membership
from telegram.constants import ChatType
from services.market import (
    get_price,
    get_forex_price,
    get_all_forex_pairs,
    get_commodity_price,
    get_usdt_toman,
    search_coins,
    find_coin_by_name
)
from bot.keyboards import (
    home_keyboard,
    markets_keyboard,
    commodities_keyboard
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

    data = get_price(coin["id"])

    if not data:
        await update.message.reply_text(
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
            f"\n🇮🇷 قیمت تقریبی تومان: "
            f"<b>{toman_price:,.0f}</b> تومان"
        )

    change_emoji = "📈" if change >= 0 else "📉"

    text = (
        f"🪙 <b>{coin['name']} ({coin['symbol'].upper()})</b>\n\n"
        f"💵 قیمت دلار: <b>${usd:,.2f}</b>"
        f"{toman_text}\n"
        f"{change_emoji} تغییر ۲۴ ساعته: "
        f"<b>{change:.2f}%</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
    )

async def send_forex(update: Update, pair: str):

    data = get_forex_price(pair)

    if not data:
        await update.message.reply_text(
            "❌ خطا در دریافت قیمت."
        )
        return


    price = data["price"]
    change = data["change"]


    change_emoji = "📈" if change >= 0 else "📉"


    text = (
        f"💱 <b>{pair}</b>\n\n"
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


    if text == "📊 بازارها":

        await update.message.reply_text(
            "نوع بازار را انتخاب کن 👇",
            reply_markup=markets_keyboard(),
        )


    elif text == "🪙 کریپتو":

        context.user_data["waiting_crypto"] = True

        await update.message.reply_text(
            "🪙 نام یا نماد ارز را وارد کنید.\n\n"
            "مثال:\n"
            "• BTC\n"
            "• ETH\n"
            "• SOL\n"
            "• PEPE\n"
            "• Bitcoin\n"
            "• Ethereum",
            reply_markup=None,
        )





    elif text == "🛢 نفت و کالا":

        await update.message.reply_text(
            "کالای موردنظر را انتخاب کن 👇",
            reply_markup=commodities_keyboard()
        )


    elif text == "🔙 بازگشت":

        context.user_data.pop("waiting_crypto", None)
        context.user_data.pop("waiting_forex", None)

        await update.message.reply_text(
            "منوی اصلی",
            reply_markup=home_keyboard(),
        )


    elif text == "💵 فارکس":

        context.user_data.pop(
            "waiting_crypto",
            None
        )

        context.user_data["waiting_forex"] = True

        await update.message.reply_text(
            "💱 نماد فارکس را وارد کنید.\n\n"
            "مثال:\n"
            "EUR\n"
            "GBP\n"
            "EUR/USD\n"
            "USD/JPY"
        )


    elif text in COMMODITIES:

        await send_commodity(
            update,
            text
        )


    elif context.user_data.get("waiting_forex"):

        query = text.upper().strip()

        pairs = get_all_forex_pairs()


        # اگر کاربر مستقیم جفت ارز زد
        if query in pairs:

            await send_forex(
                update,
                query
            )


        else:

            # اگر فقط اسم ارز زد مثل EUR
            results = [
                pair
                for pair in pairs
                if query in pair.replace("/", "")
            ]


            if len(results) == 1:

                await send_forex(
                    update,
                    results[0]
                )


            elif len(results) > 1:

                await update.message.reply_text(
                    "💱 جفت ارزهای پیدا شده:\n\n"
                    + "\n".join(results[:20])
                )


            else:

                await update.message.reply_text(
                    "❌ ارز پیدا نشد."
                )


    elif context.user_data.get("waiting_crypto"):

        query = text.strip()
        normalized_query = query.lower()

        # اگر نام کامل وارد شده باشد (Bitcoin, ethereum, ...)
        coin = find_coin_by_name(normalized_query)

        if coin:
            await send_price(update, coin)
            return

        # در غیر این صورت با نماد یا عبارت جستجو کن
        coins = search_coins(query)

        if not coins:
            await update.message.reply_text(
                "❌ ارز پیدا نشد.\n"
                "لطفاً نام یا نماد ارز را دوباره وارد کنید."
            )
            return

        if len(coins) == 1:
            await send_price(update, coins[0])
            return

        message = "🔍 چند ارز با این نماد پیدا شد:\n\n"

        for i, coin in enumerate(coins[:10], start=1):
            message += (
                f"{i}️⃣ {coin['name']} "
                f"({coin['symbol'].upper()})\n"
            )

        message += "\nلطفاً نام کامل ارز را وارد کنید."

        await update.message.reply_text(message)

    else:
        return