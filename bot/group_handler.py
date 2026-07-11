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
🤖 Crypto Price Bot فعال شد!

📈 دریافت قیمت لحظه‌ای بازارها در گروه


🪙 ارزهای دیجیتال:

🟠 بیت‌کوین (BTC)
🔵 اتریوم (ETH)
🟢 تتر (USDT)
🟡 بایننس کوین (BNB)
⚪ ریپل (XRP)
🟤 دوج کوین (DOGE)
🔷 تون کوین (TON)
🟣 سولانا (SOL)


💱 فارکس:

🇪🇺 EUR/USD
🇬🇧 GBP/USD
🇯🇵 USD/JPY
🇦🇺 AUD/USD
🇨🇦 USD/CAD


🛢 کالاها:

🟡 طلا
⚪ نقره
🛢 نفت برنت
🛢 نفت WTI
🟤 مس
🔴 گاز طبیعی


💡 نمونه درخواست:

قیمت بیت کوین

طلا

ETH

EUR/USD


📱 برای امکانات کامل:
در چت خصوصی ربات /start را بزنید.


⚡ Crypto Price Bot
"""
        )