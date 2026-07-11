from telegram import Update
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

from settings.admin_manager import (
    add_admin,
    remove_admin,
    get_admins,
)

from settings.settings_keyboard import (
    settings_keyboard,
    admin_keyboard,
)


# =========================
# States
# =========================

ADD_ADMIN_ID = 1
REMOVE_ADMIN_ID = 2



# =========================
# Open Settings Panel
# باز کردن پنل تنظیمات
# =========================

async def open_settings(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(
        text="⚙️ تنظیمات ربات",
        reply_markup=settings_keyboard()
    )



# =========================
# Admin Management Menu
# منوی مدیریت ادمین
# =========================

async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.edit_message_text(
        text="👥 مدیریت ادمین‌ها",
        reply_markup=admin_keyboard()
    )



# =========================
# Add Admin Start
# =========================

async def add_admin_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(
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

    telegram_id = update.message.text


    try:

        telegram_id = int(telegram_id)


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
            "✅ ادمین با موفقیت اضافه شد"
        )

    else:

        await update.message.reply_text(
            "⚠️ این کاربر قبلاً ادمین است"
        )


    return ConversationHandler.END



# =========================
# Remove Admin Start
# =========================

async def remove_admin_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    await query.message.reply_text(
        "➖ آیدی ادمینی که می‌خواهید حذف کنید را بفرستید:"
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
            "❌ آیدی نامعتبر است"
        )

        return REMOVE_ADMIN_ID



    result = remove_admin(
        telegram_id
    )


    if result:

        await update.message.reply_text(
            "✅ ادمین حذف شد"
        )

    else:

        await update.message.reply_text(
            "⚠️ ادمین پیدا نشد"
        )


    return ConversationHandler.END



# =========================
# List Admins
# =========================

async def list_admins(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    admins = get_admins()


    if not admins:

        text = "❌ هیچ ادمینی ثبت نشده"

    else:

        text = "📋 لیست ادمین‌ها:\n\n"

        for admin in admins:

            username = (
                f"@{admin.username}"
                if admin.username
                else "بدون یوزرنیم"
            )


            text += (
                f"👤 {username}\n"
                f"🆔 {admin.telegram_id}\n\n"
            )


    await query.edit_message_text(
        text=text,
        reply_markup=admin_keyboard()
    )



# =========================
# Register Handlers
# =========================

def settings_handlers():

    return [

        CallbackQueryHandler(
            open_settings,
            pattern="settings"
        ),


        CallbackQueryHandler(
            admin_panel,
            pattern="admin_panel"
        ),


        CallbackQueryHandler(
            list_admins,
            pattern="list_admins"
        ),


        ConversationHandler(

            entry_points=[
                CallbackQueryHandler(
                    add_admin_start,
                    pattern="add_admin"
                )
            ],

            states={

                ADD_ADMIN_ID:[
                    MessageHandler(
                        filters.TEXT,
                        add_admin_save
                    )
                ]

            },

            fallbacks=[]
        ),


        ConversationHandler(

            entry_points=[
                CallbackQueryHandler(
                    remove_admin_start,
                    pattern="remove_admin"
                )
            ],

            states={

                REMOVE_ADMIN_ID:[
                    MessageHandler(
                        filters.TEXT,
                        remove_admin_save
                    )
                ]

            },

            fallbacks=[]
        )
    ]