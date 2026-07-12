from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

from settings.admin_manager import (
    add_admin,
    remove_admin,
    get_admins,
    is_admin
)

from settings.settings_keyboard import (
    settings_keyboard,
    admin_keyboard,
    channel_keyboard
)
from settings.channel_manager import (
    add_channel,
    remove_channel,
    get_channels,
)


# =========================
# States
# =========================

ADD_ADMIN_ID = 1
REMOVE_ADMIN_ID = 2
ADD_CHANNEL = 3
REMOVE_CHANNEL = 4



# =========================
# Open Settings
# =========================

async def open_settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not is_admin(
        update.effective_user.id
    ):

        await update.message.reply_text(
            "❌ شما دسترسی ورود به تنظیمات را ندارید"
        )

        return


    await update.message.reply_text(
        "⚙️ پنل تنظیمات",
        reply_markup=settings_keyboard()
    )



# =========================
# Admin Panel
# =========================

async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "👥 مدیریت ادمین‌ها",
        reply_markup=admin_keyboard()
    )



# =========================
# Channel Panel
# =========================

async def channel_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📢 مدیریت کانال‌ها",
        reply_markup=channel_keyboard()
    )
# =========================
# Add Channel Start
# =========================

async def add_channel_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📢 لینک یا یوزرنیم کانال را ارسال کنید.\n\n"
        "مثال:\n"
        "@MyChannel\n"
        "یا\n"
        "https://t.me/MyChannel"
    )

    return ADD_CHANNEL


# =========================
# Add Channel Save
# =========================

async def add_channel_save(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text.strip()

    if text.startswith("https://t.me/"):
        username = text.split("/")[-1]
    elif text.startswith("@"):
        username = text[1:]
    else:
        username = text

    try:

        chat = await context.bot.get_chat(f"@{username}")

        result = add_channel(
            channel_id=chat.id,
            username=chat.username,
            title=chat.title
        )

        if result:

            await update.message.reply_text(
                f"✅ کانال اضافه شد.\n\n"
                f"📢 {chat.title}\n"
                f"🆔 {chat.id}",
                reply_markup=channel_keyboard()
            )

        else:

            await update.message.reply_text(
                "⚠️ این کانال قبلاً ثبت شده است.",
                reply_markup=channel_keyboard()
            )

    except TelegramError:

        await update.message.reply_text(
            "❌ کانال پیدا نشد یا ربات عضو کانال نیست.",
            reply_markup=channel_keyboard()
        )

    return ConversationHandler.END
# =========================
# Remove Channel Start
# =========================

async def remove_channel_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "➖ لینک یا یوزرنیم کانال را ارسال کنید.\n\n"
        "مثال:\n"
        "@MyChannel\n"
        "یا\n"
        "https://t.me/MyChannel"
    )

    return REMOVE_CHANNEL

# =========================
# Remove Channel Save
# =========================

async def remove_channel_save(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text.strip()

    # استخراج یوزرنیم از لینک یا @
    if text.startswith("https://t.me/"):
        username = text.split("/")[-1]
    elif text.startswith("@"):
        username = text[1:]
    else:
        username = text

    try:

        chat = await context.bot.get_chat(f"@{username}")

    except TelegramError:

        await update.message.reply_text(
            "❌ کانال پیدا نشد یا ربات عضو کانال نیست.",
            reply_markup=channel_keyboard()
        )

        return REMOVE_CHANNEL

    result = remove_channel(chat.id)

    if result:

        await update.message.reply_text(
            "✅ کانال با موفقیت حذف شد.",
            reply_markup=channel_keyboard()
        )

    else:

        await update.message.reply_text(
            "⚠️ این کانال در لیست کانال‌های اجباری ثبت نشده است.",
            reply_markup=channel_keyboard()
        )

    return ConversationHandler.END

# =========================
# Add Admin Start
# =========================

async def add_admin_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "➕ آیدی عددی ادمین جدید را ارسال کنید:"
    )

    return ADD_ADMIN_ID



# =========================
# Add Admin Save
# =========================

async def add_admin_save(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        telegram_id = int(
            update.message.text
        )

    except ValueError:

        await update.message.reply_text(
            "❌ آیدی باید عدد باشد"
        )

        return ADD_ADMIN_ID



    result = add_admin(
        telegram_id=telegram_id,
        added_by=update.effective_user.id
    )


    if result:

        await update.message.reply_text(
            "✅ ادمین اضافه شد",
            reply_markup=admin_keyboard()
        )

    else:

        await update.message.reply_text(
            "⚠️ این کاربر قبلاً ادمین است",
            reply_markup=admin_keyboard()
        )


    return ConversationHandler.END



# =========================
# Remove Admin Start
# =========================

async def remove_admin_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "➖ آیدی ادمینی که حذف شود را ارسال کنید:"
    )

    return REMOVE_ADMIN_ID



# =========================
# Remove Admin Save
# =========================

async def remove_admin_save(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        telegram_id = int(
            update.message.text
        )

    except ValueError:

        await update.message.reply_text(
            "❌ آیدی باید عدد باشد"
        )

        return REMOVE_ADMIN_ID



    result = remove_admin(
        telegram_id
    )


    if result:

        await update.message.reply_text(
            "✅ ادمین حذف شد",
            reply_markup=admin_keyboard()
        )

    else:

        await update.message.reply_text(
            "⚠️ ادمین پیدا نشد",
            reply_markup=admin_keyboard()
        )


    return ConversationHandler.END



# =========================
# List Admins
# =========================

async def list_admins(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    admins = get_admins()


    if not admins:

        text = "❌ هیچ ادمینی ثبت نشده"

    else:

        text = "📋 لیست ادمین‌ها:\n\n"

        for admin in admins:

            text += (
                f"🆔 {admin.telegram_id}\n"
            )


    await update.message.reply_text(
        text,
        reply_markup=admin_keyboard()
    )



# =========================
# Back To Settings
# =========================

async def back_settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "⚙️ پنل تنظیمات",
        reply_markup=settings_keyboard()
    )



# =========================
# Register Handlers
# =========================

def settings_handlers():

    return [

        # ورود به تنظیمات
        MessageHandler(
            filters.Regex("^⚙️ تنظیمات$"),
            open_settings
        ),


        # منوی ادمین
        MessageHandler(
            filters.Regex("^👥 مدیریت ادمین‌ها$"),
            admin_panel
        ),


        # منوی کانال
        MessageHandler(
            filters.Regex("^📢 کانال‌های اجباری$"),
            channel_panel
        ),

        # لیست ادمین
        MessageHandler(
            filters.Regex("^📋 لیست ادمین‌ها$"),
            list_admins
        ),


        # بازگشت
        MessageHandler(
            filters.Regex("^🔙 بازگشت$"),
            back_settings
        ),

        ConversationHandler(

            entry_points=[

                MessageHandler(
                    filters.Regex("^➕ اضافه کردن ادمین$"),
                    add_admin_start
                ),

                MessageHandler(
                    filters.Regex("^➖ حذف ادمین$"),
                    remove_admin_start
                )

            ],


            states={

                ADD_ADMIN_ID: [

                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        add_admin_save
                    )

                ],


                REMOVE_ADMIN_ID: [

                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        remove_admin_save
                    )

                ]

            },


            fallbacks=[]

)
    ]