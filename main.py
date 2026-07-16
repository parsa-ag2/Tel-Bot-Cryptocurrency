import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    filters
)
from telegram.ext import CallbackQueryHandler
from bot.membership import check_membership_callback
from config import BOT_TOKEN
from database.db import init_db
from bot.handlers import (
    start,
    text_handler,
    chart_callback
)
from bot.group_handler import bot_added
from bot.message_handler import market_message_handler
from settings.settings_panel import settings_handlers


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():

    # =========================
    # Database Initialize
    # =========================

    init_db()


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )


    # =========================
    # Start Command
    # =========================

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # =========================
    # Group Market Messages
    # =========================

    app.add_handler(
        MessageHandler(
            filters.ChatType.GROUPS
            & filters.TEXT
            & ~filters.COMMAND,
            market_message_handler
        ),
        group=0
    )

    # =========================
    # Private Menu
    # =========================

    app.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE
            & filters.TEXT
            & ~filters.COMMAND,
            text_handler
        ),
        group=1
    )


    # =========================
    # Bot Added To Group
    # =========================

    app.add_handler(
        ChatMemberHandler(
            bot_added,
            ChatMemberHandler.MY_CHAT_MEMBER
        )
    )



    # =========================
    # Chart Callback
    # =========================

    app.add_handler(
        CallbackQueryHandler(
            chart_callback,
            pattern="^chart_"
        )
    )

    # =========================
    # Settings Panel
    # =========================

    for handler in settings_handlers():
        app.add_handler(handler)

    # =========================
    # Membership Callback
    # =========================

    app.add_handler(
        CallbackQueryHandler(
            check_membership_callback,
            pattern="^check_membership$"
        )
    )

    logger.info(
        "✅ Bot is running..."
    )

    app.run_polling(
        allowed_updates=[
            "message",
            "callback_query",
            "my_chat_member"
        ]
)

if __name__ == "__main__":
    main()