from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.constants import ChatMemberStatus

from telegram.ext import ContextTypes

from settings.channel_manager import get_channels

from bot.keyboards import home_keyboard

# =========================
# Check User Membership
# =========================

async def check_user_membership(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    channels = get_channels()

    # اگر هیچ کانال اجباری ثبت نشده بود
    if not channels:
        return True

    not_joined = []

    for channel in channels:

        try:

            member = await context.bot.get_chat_member(
                chat_id=channel.channel_id,
                user_id=user_id
            )

            if member.status not in (
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            ):
                not_joined.append(channel)

        except Exception:

            not_joined.append(channel)

    # اگر عضو همه کانال‌ها بود
    if not not_joined:
        return True

    keyboard = []

    for channel in not_joined:

        if channel.username:

            keyboard.append([
                InlineKeyboardButton(
                    text=f"📢 {channel.title}",
                    url=f"https://t.me/{channel.username}"
                )
            ])

    keyboard.append([
        InlineKeyboardButton(
            text="✅ بررسی مجدد عضویت",
            callback_data="check_membership"
        )
    ])

    text = (
        "🚫 برای استفاده از ربات ابتدا باید در کانال‌های زیر عضو شوید.\n\n"
        "پس از عضویت روی دکمه «✅ بررسی مجدد عضویت» بزنید."
    )

    if update.callback_query:

        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif update.message:

        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    return False

# =========================
# Check Membership Callback
# =========================

async def check_membership_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    allowed = await check_user_membership(
        update,
        context
    )

    if not allowed:
        return

    await query.edit_message_text(
        "✅ عضویت شما با موفقیت تایید شد."
    )

    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="سلام 👋 به ربات خوش اومدی!",
        reply_markup=home_keyboard()
    )