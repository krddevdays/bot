#!/usr/bin/env python3

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    MessageReactionHandler,
    filters,
)

from krddevbot import settings
from krddevbot.antispam import antispam_reactions_checking, greet_chat_members
from krddevbot.logging import init_logging
from krddevbot.message_formatter import md
from krddevbot.request import HTTPXRequestWithRetry
from krddevbot.messages import track_user_messages
from krddevbot.antispam.constance import (
    HELP_MESSAGE_TEMPLATE,
    LIST_MESSAGE_TEMPLATE,
    RULES_MESSAGE_TEMPLATE
)

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /ping is issued."""
    await update.message.reply_text(
        md("I'm alive, {username}!", user=update.effective_user),
        parse_mode=ParseMode.MARKDOWN_V2
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        HELP_MESSAGE_TEMPLATE
    )

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""
    await update.message.reply_text(
        LIST_MESSAGE_TEMPLATE
    )

async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /rules is issued."""
    await update.message.reply_text(
        RULES_MESSAGE_TEMPLATE
    )


if __name__ == "__main__":
    init_logging()
    application = Application.builder()\
        .token(settings.BOT_TOKEN)\
        .request(HTTPXRequestWithRetry())\
        .get_updates_request(HTTPXRequestWithRetry())\
        .build()

    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("rules", list_command))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageReactionHandler(antispam_reactions_checking))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user_messages))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
