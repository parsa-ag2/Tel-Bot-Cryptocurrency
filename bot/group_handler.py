from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus


async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_member = update.my_chat_member

    if (
        chat_member.new_chat_member.status
        in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
        )
        and chat_member.old_chat_member.status
        in (
            ChatMemberStatus.LEFT,
            ChatMemberStatus.BANNED,
        )
    ):

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="""
🤖 ربات قیمت بازار فعال شد!


📊 برای دریافت قیمت، فقط اسم یا نماد ارز، کالا یا جفت ارز را ارسال کنید.


نمونه‌ها:


🪙 ارز دیجیتال:

BTC
ETH
SOL
DOGE
بیت کوین


💱 فارکس:

EUR/USD
EURUSD
GBPUSD
JPY


🛢 کالاها:

طلا
نقره
نفت
مس


مثال:

قیمت BTC

طلا

EURUSD


ربات قیمت لحظه‌ای را نمایش می‌دهد 📈


⚡ Market Price Bot
"""
        )
        