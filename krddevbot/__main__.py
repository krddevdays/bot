#!/usr/bin/env python3

from telegram import Update
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    MessageHandler,
    MessageReactionHandler,
    filters
)

from krddevbot import settings
from krddevbot.antispam import antispam_reactions_checking, greet_chat_members
from krddevbot.logging import init_logging
from krddevbot.message_formatter import md
from krddevbot.request import HTTPXRequestWithRetry
from krddevbot.messages import track_user_messages
from krddevbot.commands import ping_command, help_command, list_command, rules_command


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
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageReactionHandler(antispam_reactions_checking))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_user_messages))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
